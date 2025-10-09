import re
from typing import Literal
from khmer_nlp_toolkits.utils.keywords import ALDULT_KW


ADULT_URL_FILTER = re.compile(rf"(?:{'|'.join(re.escape(k) for k in ALDULT_KW)})", re.IGNORECASE)


def document_filtering(obj: dict, quality_type: Literal["High", "Medium", "Low"] = "High"):
    # No content
    if not obj["content"]:
        return None
    # adult url filtering
    url = obj["url"] if obj.get("url", False) else obj["warc_headers"]["warc-target-uri"]
    if is_adult_url_filter(url):
        return None
    # document quality classify and filtering
    paras = obj["content"].split("៕")
    qual = classify_doc_quality(len(paras), obj["metadata"]["quality_warnings"])
    if qual != quality_type:
        return None
    return obj


def classify_doc_quality(len_parag: int, quality_warning: list):
    """
    This funciton is to classify data into 3 levels of data quality.
    low - Low quality article data (contain header, footer and short_sentences of quality warning)
    medium - Medium quality article data (contain noisy of quality warning or contain multiple paragraphs)
    high - high quality article data (No quality warning and contain one paragraph info)

    Notes
    =====
    - In news article, Most of the time, the content of article end with ៕.
    - but most of the time, they include metadata of author at the end of paragraph.
    - there are few that use ៕ instead of ។, which lead to confusion.
    - Some article are a summary to news over a period of time, which is include many paragraph of
    different domain together. those are the article with 4 paragraph or more.
    - While some are an extra information add on to the main paragraph. those mostly are 2 and 3 paragraph article.
    - A few article is affected from website sracping structure which is include caption of image (end with ៕)
    in the middle of content.
    """
    if not quality_warning:
        if len_parag <= 2:
            return "High"
        else:
            return "Medium"
    if "header" in quality_warning or "footer" in quality_warning or "short_sentences" in quality_warning:
        return "Low"
    if "noisy" in quality_warning or len_parag > 2:
        return "Medium"
    return "High"


def is_adult_url_filter(url: str):
    """
    Check if the url are appropriate content.

    Parameters
    ==========
    url: str
        url string to check for keyword.

    Return
    ======
    bool
        True if the url content keyword, vise versa.
    """
    return url and bool(ADULT_URL_FILTER.search(url))
