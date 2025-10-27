from khmer_nlp_toolkits.utils import get_filepath, lazy_read_jsonl

filepaths = get_filepath("data/high/doc_dedup")

with open("data/high/corpus.txt", "w") as writer:
    for file in filepaths:
        for obj in lazy_read_jsonl(file):
            if obj is None:
                continue
            writer.write(obj["content"] + "\n")
