"""
Document filtering module.
"""
import re
from typing import Literal

from khmer_nlp_toolkits.utils.keywords import ALDULT_KW
from khmer_nlp_toolkits.commoncrawl.quality_warning import WARNING_FLAGSET


ADULT_URL_FILTER = re.compile(rf"(?:{'|'.join(re.escape(k) for k in ALDULT_KW)})", re.IGNORECASE)


def document_filtering(obj: dict, quality_type: Literal["High", "Medium", "Low"] = "High"):
    """
    Classify and filter those not match in quality.
    """
    # No content
    if not obj["content"]:
        return None

    # adult url filtering
    url = obj["url"] if obj.get("url", False) else obj["warc_headers"]["warc-target-uri"]
    if is_adult_url_filter(url):
        return None

    # document quality classify and filtering
    qual = classify_doc_quality(obj["metadata"]["quality_warnings"])
    if qual != quality_type:
        return None

    return obj


def classify_doc_quality(quality_warning: list[str]):
    """
    This funciton is to classify data into 3 levels of data quality.
    low - Low quality article data (contain short_sentences of quality warning)
    medium - Medium quality article data (contain noisy, header, footer of quality warning)
    high - high quality article data (contain tiny or none quality warning)

    Parameter:
    quality_warning: list[str]
    """
    if not isinstance(quality_warning, list):
        raise TypeError("quality_warning must be list of string.")
    if any(flag not in WARNING_FLAGSET for flag in quality_warning):
        raise ValueError("Got unexpected warning flags. See quality_warning for flag info.")

    # Warning quality flags base check
    if "short_sentences" in quality_warning:
        return "Low"
    if any(flag in quality_warning for flag in ["noisy", "header", "footer"]):
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
