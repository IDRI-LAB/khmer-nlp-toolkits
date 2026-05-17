import __init__
import tqdm
import jsonlines

from khmer_nlp_toolkits.deduplicate.url_dedup import is_url_duplicate, write_hash_file
from khmer_nlp_toolkits.utils import get_filepath, lazy_read_jsonl


SRC = "/home/m-psi/heangs/workspace/data/scrape_data"
DST = "/home/m-psi/heangs/workspace/khmer-nlp-toolkits/data/raw/dataset.jsonl"


filepaths = get_filepath(SRC)


temp = []
with jsonlines.open(DST, "a") as writer:
    for file in filepaths:
        print(file)
        for obj in tqdm.tqdm(lazy_read_jsonl(file), ncols=100):
            if obj is None:
                continue
            is_dup, hash = is_url_duplicate(obj["url"], rt_hash=True)
            if is_dup:
                continue
            obj["id"] = hash
            writer.write(obj)

write_hash_file()
