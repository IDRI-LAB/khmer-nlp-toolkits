"""
This script is designed to clean Common Crawl data specifically for Khmer language text.
"""
import os
import tqdm
import time
import jsonlines
import subprocess
import datetime
from khmer_nlp_toolkits.pipeline import Pipeline
from khmer_nlp_toolkits.commoncrawl.document_filtering import document_filtering
from khmer_nlp_toolkits.commoncrawl.feature_cleaning import run as clean_cc
from khmer_nlp_toolkits.text.anonymize import run as anonymise
from khmer_nlp_toolkits.text.clean import run as clean_text
from khmer_nlp_toolkits.text.normalize import run as normalization



def main(in_path, out_path):
    """
    Main function to execute the cleaning pipeline on Common Crawl data.
    It initializes the pipeline, reads input data from a JSONL file, processes it,
    and writes the cleaned output to another JSONL file.
    The pipeline consists of two steps:
    1. `clean_cc`: Cleans Khmer data with a specified threshold for quality warnings.
    2. `clean_text`: Further cleans the text by removing URLs, repetitive punctuation,
    and miscellaneous symbols, and handles spaces appropriately.
    The cleaned data is written to 'final_data_cleaning.jsonl'.

    Return
    =======
    This script does not return any value but writes the cleaned data to a file.

    Noted
    ======
    - The cleaning pipeline is designed to handle Khmer text data specifically, ensuring that
    the text is cleaned according to the requirements of Khmer language processing.
    """
    # Adjustment between function
    def anonymise_obj(obj):
        obj["content"] = anonymise(obj["content"])
        return obj
    def clean_text_obj(obj):
        obj["content"] = clean_text(obj["content"]).replace("[ URL ]", "[URL]")
        del obj["metadata"]["sentence_identifications"]
        del obj["metadata"]["quality_warnings"]
        del obj["metadata"]["scrape_at"]
        return obj

    def normalize_obj(obj):
        obj["content"] = normalization(obj["content"])
        return obj

    # Pipeline setup
    pipeline = Pipeline()
    pipeline.add(document_filtering, quality_type="High", is_wrap=True)
    # pipeline.add(clean_cc, is_wrap=True)
    # pipeline.add(anonymise_obj, is_wrap=True)
    # pipeline.add(clean_text_obj, is_wrap=True)
    # pipeline.add(normalize_obj, num_process=15, is_wrap=True)

    # Count line for tqdm
    lines = subprocess.run(["wc", "-l", in_path], capture_output=True)
    lines = int(lines.stdout.decode("utf-8").split(" ")[0])
    # run and save
    with jsonlines.open(in_path, mode="r") as reader, jsonlines.open(out_path, "w") as writer, tqdm.tqdm(total=lines, desc="Process") as pbar:
        for batch in pipeline.run_parallel(reader.iter(allow_none=True), qsize=10, batch_size=200):
            writer.write_all(obj for obj in batch if obj is not None)
            # print(pipeline.get_queue_status())
            pbar.update(len(batch))


if __name__ == "__main__":

    # Pre and Post Pipeline
    # DATA_SOURCE = "/home/m-psi/heangs/workspace/data/scrape_data"
    DATA_SOURCE = "/home/m-psi/heangs/workspace/data/scrape_data"
    DATA_DESTINATION = "data/high/raw"
    os.makedirs(DATA_DESTINATION, exist_ok=True)
    FILE_NAME = sorted(os.listdir(DATA_SOURCE))[21:]

    filepaths_source = [os.path.join(DATA_SOURCE, f) for f in FILE_NAME]
    filepaths_destination = [os.path.join(DATA_DESTINATION, f) for f in FILE_NAME]

    for source, dest in zip(filepaths_source, filepaths_destination):
        start = datetime.datetime.now()
        print(source)
        main(source, dest)
        end = datetime.datetime.now()
        print(f"Duration: {end - start}")
