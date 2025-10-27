"""
This script is designed to clean Common Crawl data specifically for Khmer language text.
"""
import __init__
import tqdm
import jsonlines
import subprocess
import datetime
import logging

from khmer_nlp_toolkits.utils import get_filepath
from khmer_nlp_toolkits.pipeline import Pipeline
from khmer_nlp_toolkits.commoncrawl.document_filtering import document_filtering
from khmer_nlp_toolkits.text.scrape import clean as scrape_clean
from khmer_nlp_toolkits.commoncrawl.feature_cleaning import run as clean_cc
from khmer_nlp_toolkits.text.anonymize import run as anonymise
from khmer_nlp_toolkits.text.clean import run as clean_text
from khmer_nlp_toolkits.text.normalize import run as normalization
from khmernltk import word_tokenize


# logging.basicConfig(level=logging.INFO)

def main():
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

    def word_segmentation(obj):
        words = word_tokenize(obj["content"])
        obj["content"] = " ".join(word for word in words if word != " ")
        return obj

    # Pipeline setup
    pipeline = Pipeline()
    pipeline.add(document_filtering, quality_type="High", is_wrap=True)
    pipeline.add(scrape_clean, is_wrap=True)
    pipeline.add(clean_cc, is_wrap=True)
    pipeline.add(anonymise_obj, is_wrap=True)
    pipeline.add(clean_text_obj, is_wrap=True)
    pipeline.add(normalize_obj, num_process=15, is_wrap=True)
    pipeline.add(word_segmentation, is_wrap=True, num_process=15)

    return pipeline


if __name__ == "__main__":

    # Pre and Post Pipeline
    # DATA_SOURCE = "/home/m-psi/heangs/workspace/data/scrape_data"
    DATA_SOURCE = "data/high/clean"
    DATA_DESTINATION = "data/high/segment"
    filepaths = get_filepath(DATA_SOURCE, DATA_DESTINATION)

    pipeline = main()

    for source, dest in filepaths:
        start = datetime.datetime.now()
        print(source)
        # Count line for tqdm
        lines = subprocess.run(["wc", "-l", source], capture_output=True)
        lines = int(lines.stdout.decode("utf-8").split(" ")[0])
        # run and save
        with jsonlines.open(source, mode="r") as reader, jsonlines.open(dest, "w") as writer, tqdm.tqdm(total=lines, desc="Process") as pbar:
            for batch in pipeline.run_parallel(reader.iter(allow_none=True), qsize=10, batch_size=50):
                writer.write_all(obj for obj in batch if obj is not None)
                # print(pipeline.get_queue_status())
                pbar.update(len(batch))
        end = datetime.datetime.now()
        print(f"Duration: {end - start}")
