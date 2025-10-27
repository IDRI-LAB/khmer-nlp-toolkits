"""
URL Deduplication Module.
"""
import os
import hashlib
import threading


THREAD_LOCK = threading.Lock()
HASH_FILE = ".cache/seen_url.txt"
OLD_HASH = set()
NEW_HASH = set()


def url_dedup(batch_data):
    batch = []
    for obj in batch_data:
        url = obj["url"] if obj.get("url", False) else obj["warc_headers"]["warc-target-uri"]
        is_dup, hash_val = is_url_duplicate(url=url, rt_hash=True)
        if not is_dup:
            obj["id"] = hash_val
            batch.append(obj)
        else:
            batch.append(None)
    write_hash_file()
    return batch


def load_hashes_file(path=HASH_FILE):
    """
    Hash loading function to load previous seen url.
    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w"):
            pass
        return
    with open(path, "r") as reader:
        for hash_val in reader:
            OLD_HASH.add(hash_val.strip())


load_hashes_file()


def write_hash_file(path=HASH_FILE):
    """
    Overwrite update deduplicate hash to file.
    """
    with THREAD_LOCK, open(path, "a") as writer:
        OLD_HASH.update(NEW_HASH)
        for hash_val in NEW_HASH:
            writer.write(hash_val + "\n")
        NEW_HASH.clear()


def url_hashing(url: str):
    """
    Hashing URL for comparison with md5.
    """
    url = url.removeprefix("https://").removeprefix("http://").removeprefix("www.")
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def is_url_duplicate(url: str, rt_hash: bool = False):
    """
    Duplication check function. If URL was seen before, it will return True and vise versa.
    You have to call write_hash_file() after finish running to save record for later dedup or else it will be one time dedup.

    Notes
    =====
    - With batch processing, run this on normal loop is much more faster.
    - Parallel streaming process (each data pass through all steps) will that more time.
    """
    # Logic
    hash_val = url_hashing(url)
    with THREAD_LOCK:
        if hash_val in OLD_HASH or hash_val in NEW_HASH:
            return True if not rt_hash else (True, hash_val)
        NEW_HASH.add(hash_val)
    return False if not rt_hash else (False, hash_val)


if __name__ == "__main__":
    import jsonlines
    from datetime import datetime
    from concurrent.futures import ThreadPoolExecutor

    with jsonlines.open("../data/scrape_data/khmerload_20250723_140400.jsonl", "r") as file:
        t = [d["url"] for d in file]
    print(f"Total URL = {len(t)}")

    ############################
    # parallel streaming process
    ############################
    start = datetime.now()
    with ThreadPoolExecutor(max_workers=1) as exe:
        res = list(exe.map(is_url_duplicate, t))
    end = datetime.now()
    print("time", end-start)
    ###################
    #  batch processing
    ###################
    start = datetime.now()
    res = []
    for d in t:
        res.append(is_url_duplicate(d))
    end = datetime.now()
    print("time", end-start)
