"""
This script is designed to clean Common Crawl data specifically for Khmer language text.
"""
import jsonlines
from khmer-nlp-toolkits.pipeline import Pipeline
from khmer-nlp-toolkits.commoncrawl.feature_cleaning import cleaning_kh_data
from khmer-nlp-toolkits.text.clean import clean_text


def main():
    """
    Main function to execute the cleaning pipeline on Common Crawl data.
    It initializes the pipeline, reads input data from a JSONL file, processes it,
    and writes the cleaned output to another JSONL file.
    The pipeline consists of two steps:
    1. `cleaning_kh_data`: Cleans Khmer data with a specified threshold for quality warnings.
    2. `clean_text`: Further cleans the text by removing URLs, repetitive punctuation,
    and miscellaneous symbols, and handles spaces appropriately.
    The cleaned data is written to 'final_data_cleaning.jsonl'.
    Parameters
    ==========
    None
    Return
    =======
    None
    This script does not return any value but writes the cleaned data to a file.
    Noted
    ======
    - The input file 'cc_data_sample.jsonl' should be in the same directory as this script.
    - The output file 'final_data_cleaning.jsonl' will be created or overwritten in the same directory.
    - The cleaning pipeline is designed to handle Khmer text data specifically, ensuring that
      the text is cleaned according to the requirements of Khmer language processing.
    """
    pipeline = Pipeline()
    pipeline.add(cleaning_kh_data, threshold=75, desc="Cleaning Khmer data with a threshold of 75%")
    pipeline.add(clean_text, desc="Cleaning text")

    with jsonlines.open('cc_data_sample.jsonl', mode="r") as reader, \
         jsonlines.open("final_data_cleaning.jsonl", mode="w") as writer:
        for input_data in reader:
            output_data = pipeline.run(input_data)
            if output_data:
                writer.write(output_data)


if __name__ == "__main__":
    main()
