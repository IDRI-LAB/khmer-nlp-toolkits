import __init__
import datetime
import jsonlines
from multiprocessing.pool import Pool

from khmer_nlp_toolkits.utils import get_filepath
from khmer_nlp_toolkits.deduplicate.document_dedup import LSHashing, simhash_fingerprint, verify_edit_dist
from khmer_nlp_toolkits.utils import lazy_read_jsonl


def lsh_worker(batch):
    temp_lsh = LSHashing(64, 8)
    for obj in batch:
        if not obj:
            continue
        temp_lsh.indexing(simhash_fingerprint(obj["content"]), obj["id"])
    return temp_lsh


def data_parser(filepath: str, n_batch=1000):
    batch = []
    for obj in lazy_read_jsonl(filepath, show_progress=True):
        if not obj:
            continue
        batch.append(obj)
        if len(batch) == n_batch:
            yield batch
            batch = []

# Varible
DATA_DIR = "data/high/segment"

# global setup
lsh = LSHashing(64, 8)
filepaths = get_filepath(DATA_DIR)


# Parallel indexing
start = datetime.datetime.now()
with Pool(processes=25) as pool:
    for temp_lsh in pool.imap_unordered(lsh_worker, data_parser(filepaths[0])):
        lsh.combine_lsh(temp_lsh)
end = datetime.datetime.now()
print(f"Indexing time = {end-start}")
lsh.save_cache()


# Parallel finding pair
start = datetime.datetime.now()
pairs = lsh.get_dup_pairs(nprocess=25, save_file=".cache/dup_pairs.txt")
end = datetime.datetime.now()
print(f"Get pair time = {end-start}")


# verify with edit distance
start = datetime.datetime.now()
removal = verify_edit_dist(
    pair_path=".cache/dup_pairs.txt",
    datapath="data/high/segment"
)
end = datetime.datetime.now()
print(f"Verify pair time = {end-start}")


# remove dup data
start = datetime.datetime.now()
filepaths = get_filepath("data/high/segment", "data/high/dedup")
for src, des in filepaths:
    with jsonlines.open(des, "w") as writer:
        for obj in lazy_read_jsonl(src):
            if obj is None:
                continue
            if obj["id"] in removal:
                continue
            writer.write(obj)
end = datetime.datetime.now()
print(f"Remove duplicate data time = {end-start}")
