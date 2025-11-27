"""
This script is designed to clean Common Crawl data specifically for Khmer language text.
"""
import __init__
import tqdm
import jsonlines
import subprocess
import datetime
import logging

from khmer_nlp_toolkits.utils import get_filepath, lazy_read_jsonl
from khmer_nlp_toolkits.pipeline import Pipeline
from khmer_nlp_toolkits.commoncrawl.document_filtering import document_filtering
from khmer_nlp_toolkits.text.scrape import scrape_cleaner
from khmer_nlp_toolkits.text.anonymize import anonymizer
from khmer_nlp_toolkits.text.clean import text_cleaner
from khmer_nlp_toolkits.text.normalize import nomalizer
from khmer_nlp_toolkits.text.mask_lang import lang_masking
from khmernltk import word_tokenize
from segment import Tokenizer
tokenizer = Tokenizer("segment/model/morpheme_model.bin")

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
    #############################
    # Adjustment between function
    #############################
    def anonymize_obj(obj):
        obj["content"] = anonymizer(obj["content"])
        return obj

    def clean_text_obj(obj):
        obj["content"] = text_cleaner(obj["content"]).replace("[ URL ]", "[URL]")
        del obj["metadata"]
        del obj["title"]
        return obj

    def normalize_obj(obj):
        obj["content"] = nomalizer(obj["content"])
        return obj

    def word_segmentation(obj):
        words = word_tokenize(obj["content"])
        obj["content"] = " ".join(word for word in words if word != " ")
        return obj

    def word_segmentation_morpheme(obj):
        obj["content"] = tokenizer.tokenize(obj["content"])
        return obj

    def obj_lang_masking(obj):
        if not obj:
            return None
        obj["content"] = lang_masking(obj["content"])
        return obj

    ################
    # Pipeline setup
    ################
    pipeline = Pipeline()
    pipeline.add(document_filtering, quality_type="High", is_wrap=True) # doc quality filter

    pipeline.add(scrape_cleaner, is_wrap=True)  # spider characteristic clean
    pipeline.add(anonymize_obj, is_wrap=True, num_process=2)  # masking url and email

    pipeline.add(normalize_obj, num_process=20, is_wrap=True)
    pipeline.add(clean_text_obj, is_wrap=True, num_process=2)  # text clean
    pipeline.add(obj_lang_masking, is_wrap=True, num_process=1)

    pipeline.add(word_segmentation_morpheme, is_wrap=True, num_process=30)

    return pipeline


if __name__ == "__main__":

    # Pre and Post Pipeline
    DATA_SOURCE = "data/high/"
    DATA_DESTINATION = "data/high/lang_mask"
    filepaths = get_filepath(DATA_SOURCE, DATA_DESTINATION)

    pipeline = main()

    for source, dest in filepaths:
        start = datetime.datetime.now()
        print(source)
        # run and save
        with jsonlines.open(dest, "w") as writer:
            reader = lazy_read_jsonl(source, show_progress=True)
            for batch in pipeline.run_parallel(reader, qsize=20, batch_size=250):
                writer.write_all(obj for obj in batch if obj is not None)
                # print(pipeline.get_queue_status())
        end = datetime.datetime.now()
        print(f"Duration: {end - start}")
