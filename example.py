"""
This script is designed to clean Common Crawl data specifically for Khmer language text.
"""
import os
import jsonlines
from khmer_nlp_toolkits.pipeline import Pipeline
from khmer_nlp_toolkits.commoncrawl.feature_cleaning import run as clean_cc
from khmer_nlp_toolkits.text.clean import run as clean_text


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
    def align_clean_text(obj):
        if obj:
            obj["content"] = clean_text(obj["content"])
            return obj

    # Pipeline
    pipeline = Pipeline()
    pipeline.add(clean_cc, threshold=75, is_dedup=True, desc="Cleaning Khmer data with a threshold of 75%")
    pipeline.add(align_clean_text, desc="Cleaning text")

    # Pre and Post Pipeline
    DATA_PATH = "/Users/sopagna/workspace/Data/cadt_scrape/scrape_data"
    dirs = os.listdir(DATA_PATH)
    for d in dirs:
        print(d)
        with jsonlines.open(os.path.join(DATA_PATH, d), mode="r") as reader, \
            jsonlines.open("final_data_cleaning.jsonl", mode="a") as writer:
            for input_data in reader:
                output_data = pipeline.run(input_data)
                if output_data:
                    writer.write(output_data)


if __name__ == "__main__":
    main()
