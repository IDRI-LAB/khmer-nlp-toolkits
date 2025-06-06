from pipeline import Pipeline
from src.commoncrawl.feature_cleaning import cleaning_kh_data


def main():
    pipeline = Pipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
