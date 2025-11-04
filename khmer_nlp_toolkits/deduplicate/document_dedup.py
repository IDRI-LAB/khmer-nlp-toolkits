import os
import mmh3
import pickle
import jsonlines
import numpy as np
from tqdm import tqdm
from typing import Literal, Any
from ngram import NGram
from simhash import Simhash
from itertools import combinations, islice
from collections import Counter, defaultdict
from rapidfuzz.distance import Levenshtein
from multiprocessing import Pool
from khmer_nlp_toolkits.utils import get_filepath
from lmdbdict import LMDBDict
from khmer_nlp_toolkits.utils import lazy_read_jsonl


# patch SimHash package
# Increase bit Cumulative value from uint8 -> uint16
Simhash._bitarray_from_bytes = staticmethod(lambda b: np.unpackbits(np.frombuffer(b, dtype='>B')).astype(np.int16))
DB_CACHE = ".cache/dedup_data.lmdb"
os.makedirs(".cache/", exist_ok=True)


def hash_mmh3(x: str):
    """
    MurmurHash3 function called.

    Parameters
    ==========
    x: str
        String to hash

    Return
    ======
    unsigned 64-bit MurmurHash3

    Noted
    =====
    mmh3 return [64lsb, 64msb] of internal hash128 but it is different from .hash128().
    Normally, it was used 64lsb (index 0) of .hash64().
    In python, signed number do not apply 2 complimented and use sign symbol - for negative value
    and no symbol for positive value. And python remove zero leading from bin.
    This mean: -7 == -0b111 (with zero leading -0b0111) for signed int
    while -7 == 0b1001 for 4bits unsigned int.
    Checkout python arithmetic vs bitwise operation.
    """
    return mmh3.hash64(x)[0] & 0xFFFFFFFFFFFFFFFF


def simhash_fingerprint(text, n: int = 2, rt_type: Literal["bit", "vec"] = None):
    """
    
    """
    tokens = text.split(" ")
    ngram = NGram(N=n)
    weights = Counter(" ".join(gram) for gram in ngram.ngrams(tokens))
    hash_obj = Simhash(weights.items(), hashfunc=hash_mmh3)
    if rt_type == "bit": 
        return bin(hash_obj.value)[2:].zfill(64)
    elif rt_type == "vec":
        return [int(bit) for bit in bin(hash_obj.value)[2:].zfill(64)]
    return hash_obj.value

def hamming_dist(x: int, y: int, rt_similarity: bool = False):
    """
    Calculate hamming distance of 2 value.

    Parameters
    ==========
    x, y: int
        Simahash fingerprint.
    total_bit: int
        Total bit length to calculate similarity.
    Return
    ======
    int
        The distance between x,y (Bitwise different).
    """
    if isinstance(x, str) or isinstance(y, str):
        x = int(x)
        y = int(y)
    if rt_similarity:
        return 1 - (x ^ y).bit_count()/64
    return (x ^ y).bit_count()


class LSHashing():
    def __init__(self, input_dim, bitlen):
        if input_dim < bitlen:
            # change this to division
            raise ValueError("input dimension can not smaller than bitlen")
        self.bitlen = bitlen
        self.input_dim = input_dim
        self.cluster = {i:defaultdict(set) for i in range(int(input_dim/bitlen))}

    def indexing(self, fingerprint, identity: str):
        if isinstance(fingerprint, str):
            if len(fingerprint) != self.input_dim:
                raise ValueError(f"Fingerprint len is not equal to input_dim")
            fingerprint = int(fingerprint, base=2)
        elif isinstance(fingerprint, int) and fingerprint.bit_length() > self.input_dim:
            raise ValueError(f"Fingerprint bit length is bigger that input_dim")

        doc = str(identity) + "--" + str(fingerprint)
        mask = (1 << self.bitlen) - 1
        for band_idx in range(self.input_dim // self.bitlen):
            bucket = (fingerprint >> (band_idx*self.bitlen)) & mask
            self.cluster[band_idx][bucket].add(doc)

    def combine_lsh(self, lsh):
        for band in lsh.cluster.keys():
            for bucket in lsh.cluster[band].keys():
                self.cluster[band][bucket].update(lsh.cluster[band][bucket])

    def load_cache(self, name: str = None):
        cachepath = f".cache/{name}.pkl" if name else ".cache/lsh_indexing.pkl"
        with open(cachepath, "rb") as file:
            self.cluster = pickle.load(file)

    def save_cache(self, name: str = None):
        cachepath = f".cache/{name}.pkl" if name else ".cache/lsh_indexing.pkl"
        with open(cachepath, "wb") as file:
            pickle.dump(self.cluster, file)

    @staticmethod
    def _bucket_dedup(bucket: list[str], threshold: float = 0.9):
        """
        This function is design as a staticmethod for parallel purpose in self.get_dup_pair().

        Parameters
        ==========
        bucket: list[str]
            lsh bucket after indexing.
        threshold: float
            Threshold for hamming similarity filter check.

        Return
        ======
        set()
            A set of candidate pair after filtering.
        """
        bucket = [doc.split("--") for doc in bucket]
        bucket_pair = set()
        for [id1, fp1], [id2, fp2] in combinations(bucket, 2):
            if hamming_dist(fp1, fp2, rt_similarity=True) < threshold:
                continue
            bucket_pair.add(id1+"-"+id2 if id1>id2 else id2+"-"+id1)
        return bucket_pair

    def _bucket_feeder(self, band_idx: int = None):
        """
        Lazy bucket feeder for parallel purpose in self.get_dup_pairs().

        Parameters
        ==========
        band_idx: int|None, default=None
            Collect bucket of all bands if None, else collect only given band_idx.

        Yield
        ======
        Generator(list[str])
            loop yield data of each bucket.
        """
        if band_idx is None:
            bands = self.cluster.keys()
        else:
            if band_idx not in self.cluster.keys():
                raise IndexError("Index out of bound.")
            bands = [band_idx]

        for band in bands:
            for bucket in self.cluster[band].keys():
                # print(f"==> On band {band} and bucket {bucket}")
                yield self.cluster[band][bucket]

    def get_dup_pairs(self, band_idx: int = None, save_file: str = None, nprocess: int = 1):
        """
        Get the pairs candidate in buckets.

        Return
        ======
        set[str]|None
            Return the near-similar pairs. if given save_file return None.
        """
        if band_idx and band_idx > self.input_dim // self.bitlen:
            raise IndexError("index out of range")

        save_step = 0
        dup_pair = set()
        total_bucket = sum([len(self.cluster[band]) for band in self.cluster])
        with Pool(processes=nprocess) as pool:
            for res in tqdm(pool.imap_unordered(self._bucket_dedup, self._bucket_feeder(band_idx)), total=total_bucket, ncols=70):
                dup_pair.update(res)
                save_step += 1
                if save_file and save_step % 10 == 0:
                    with open(save_file, "w") as file:
                        file.write("\n".join(dup_pair))
        if save_file:
            with open(save_file, "w") as file:
                file.write("\n".join(dup_pair))
            return None
        return dup_pair


def verify_edit_dist(pair_path: str, datapath: str, save_file:str=None, threshold: float = 0.8):
    # get unique id from pair to get actual data.
    unique_key = set()
    with open(pair_path, "r") as file:
        for pair in map(lambda x: x.strip().split("-"), file):
            unique_key.update(pair)
    # get actual data prepared for comparison
    db = LMDBDict(DB_CACHE, "w")
    filepaths = get_filepath(datapath)
    for filepath in filepaths:
        for obj in lazy_read_jsonl(filepath):
            if not obj:
                continue
            if obj["id"] in unique_key:
                db[obj["id"]] = {
                    "url": obj["url"],
                    "content": obj["content"]
                }
        db.flush()
    db = LMDBDict(DB_CACHE, "r")
    del unique_key
    # Comparison
    removal = set()
    with open(pair_path, "r") as file:
        for id1, id2 in map(lambda x: x.strip().split("-"), file):
            if id1 in removal or id2 in removal:
                continue
            if Levenshtein.normalized_similarity(db[id1]["content"], db[id2]["content"]) < threshold:
                continue
            removal.add(id1 if len(db[id1]["content"]) < len(db[id2]["content"]) else id2)
    if save_file:
        with open(save_file, "w") as file:
            file.write("\n".join(removal))
    return removal


if __name__ == "__main__":
    import jsonlines
    # ################
    # # Example SimHash FingerPrint
    # ################
    # doc = "hello world this is a test hello world"
    # sim_fp = simhash_fingerprint(doc)
    # print(f"SimHash (64-bit) value: {sim_fp}")

    # ###############
    # # Example of indexing and get duplicate pair
    # ###############
    # lsh = LSHashing(64, 8)
    # lsh.indexing(sim_fp)  # Indexing all of your data
    # dup_pairs = lsh.get_dup_pairs(threshold=0.9)  # Get all candidate of duplicate pairs

    ###############
    # Full example
    ###############
    lsh = LSHashing(64, 8)
    with jsonlines.open("your_data_file", "r") as file:
        for obj in tqdm.tqdm(file.iter(allow_none=True)):
            if not obj:
                continue
            fp = simhash_fingerprint(obj["content"])
            lsh.indexing(fp, obj["id"])
    pairs = lsh.get_dup_pairs(save_file="cache/test_run.txt", nprocess=15)  # run 15 jobs parallel and save to file.
    print(f"Got {len(pairs)} candidate pairs!")
    print("Top 5 pairs:")
    print(pairs[:5])
