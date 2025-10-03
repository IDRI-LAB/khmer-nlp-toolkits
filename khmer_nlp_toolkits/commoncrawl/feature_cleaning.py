"""
Module for apply feature cleaning on commoncrawl data structure.
"""
import re
import jsonlines
import regex
from typing import Union, List
from khmer_nlp_toolkits.text.clean import __kh_strip, count_khmer_char
from khmer_nlp_toolkits.keywords import ALDULT_KW
from khmer_nlp_toolkits.commoncrawl.quality_warning import check_quality_warning




def run(data: dict) -> List[str]:
    """
    Main Feature of Cleaning using metadata on CC to filtering out some doucments or sentences.

    Parameter
    ==========
    data: dict
        Json data of common crawl format.

    Return
    =======
    Oject data after cleaning.
    """
    try:
        if not data["content"]:
            return None

        content = paragraph_clean(data["content"])

        data.update({"content": content})
    except KeyError as err:
        raise err
    return data





def paragraph_clean(content: str):
    """
    Filter out any article with more than 2 paragraphs.

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
    paragraphs = content.rsplit("៕", 1)
    if len(paragraphs) == 1:
        return content
    return paragraphs[0] + "៕"
