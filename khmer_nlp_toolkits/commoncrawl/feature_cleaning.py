"""
Module for apply feature cleaning on commoncrawl data structure.
"""
import os
import re
import regex
import hashlib
import subprocess
from typing import Union, Optional, List, Dict
from khmer_nlp_toolkits.text.clean import __kh_strip
from khmer_nlp_toolkits.keywords import ALDULT_KW


ADULT_URL_FILTER = re.compile(rf"(?:{'|'.join(re.escape(k) for k in ALDULT_KW)})", re.IGNORECASE)


def clean_cc(data: Union[dict, list], threshold: int = 75, is_dedup: bool = True) -> List[str]:
    """
    Main Feature of Cleaning using metadata on CC to filtering out some doucments or sentences.

    Parameter
    ==========
    data: Union[dict, list]
        Json data of common crawl format.

    Return
    =======
    khmer data
    """
    try:
        # our scrape format
        if data.get("url", False):
            del data["metadata"]["scrape_at"]
            # del data["metadata"]["spider"]
        else:
            data["url"] = data["warc_headers"]["warc-target-uri"]
            del data["warc_headers"]
            del data["metadata"]["identification"]  # No need, it use for document select when download only
            del data["metadata"]["tlsh"]  # content dedup after clean
            del data["metadata"]["harmful_pp"]  # No model apply when download
            del data["metadata"]["categories"]  # No model apply when download
        url = data["url"]
        if is_adult_url_filter(url):
            return None
        if is_dedup and is_url_duplicated(url, "dedup"):
            return None
    except KeyError as err:
        raise KeyError("Key ['url'] or ['warc_headers']['warc-target-uri']") from err
    try:
        cleaned_sents = filter_kh_lng(data['content'], data['metadata']['sentence_identifications'])
        del data['metadata']['sentence_identifications']
        cleaned_sents = check_quality_warning(cleaned_sents, data['metadata']['quality_warnings'], threshold=threshold)
        if not cleaned_sents:
            return None
        del data['metadata']['quality_warnings']
        data.update({"content": cleaned_sents})
    except KeyError as err:
        raise err
    return data


def filter_kh_lng(contents: List[str], sent_idens: List[Optional[Dict[str, float]]]):
    """
    Filter data to get only the content with Khmer language label ("kh")
    and Identification data is not None.

    Parameters
    ==========
    contents: List[str]
                content for cleaning
    sent_idens: List[Optional[Dict[str, float]]]
                sentent identification to check label 'km'

    Return
    ======
    contents: List[str]
        list of content that has khmer language label 'km' and not None

    Noted
    =====
    - if content is None, it will be removed.
    - if content is not in Khmer language, it will be removed.
    - if content is not in equal length with sentence identification, it will be raise.
    """

    if not contents or not sent_idens:
        raise ValueError("Missing contents or sentence identifications")
    content_split = contents.split('\n')
    if len(content_split) != len(sent_idens):
        raise ValueError("List is not in equal lenght")
    list_data_kh = []
    for iden_data, con_data in zip(sent_idens, content_split):
        if iden_data is not None and iden_data['label'] == "km":
            list_data_kh.append(con_data)
    return list_data_kh


def check_quality_warning(sentences: List[str], qua_warning: List[str], threshold: int = 75):
    """
    check quality warninng data.

    Parameters
    ==========
    sentences: List[str]
        list of sentence for cleaning if it has quality warning
    qua_warning: List[str]
        list of quality warning
    threshold: int = 75
        threshold to filter sentence character length

    Return
    ======
    sentences: List[str]
        list of sentence for cleaning if it has quality warning

    Noted
    ======
    - if sentence has number char more than 50% of the sentence, it will be removed.
    - if sentence length is less than threshold, it will be removed.
    """

    def count_khmer_chat(sent: str):
        """
        Count existing Khmer char in context. It count only character in Khmer unicode block 1780-17FF.

        Parameters
        ==========
        sent: str
            sentence to check

        Returns
        =======
        int
            Number of Khmer character.
        """
        # return ''.join(char for char in sent if char.isdigit())
        return len(regex.findall(r"\p{khmer}", sent))

    if sentences and qua_warning:
        return [
            sent
            for sent in sentences
            if len(__kh_strip(sent)) > threshold
            and count_khmer_chat(sent) / len(sent) > 0.5
        ]
    return [__kh_strip(sent) for sent in sentences if len(sent) > threshold]


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


def is_url_duplicated(url: str, hashpath: str):
    """
    Check whether the URL is already seen before or not.

    Parameters
    ==========
    url: str
        The url string to check.
    hash_filepath: str
        The filepath where it is store the previouse seen url hash.

    Return
    ======
    bool
        True is url was seen, and vise verrsa.
    """
    # URL manipulate
    url = url.removeprefix("https://").removeprefix("http://").removeprefix("www.")
    # Hashing
    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
    filepath = os.path.join(hashpath, "url.seen")
    res = subprocess.run(['grep', '-Fxq', url_hash, filepath], stderr=subprocess.PIPE)
    if res.returncode == 0:
        return True
    elif res.returncode in (1, 2):
        if res.returncode == 2:
            os.makedirs(hashpath, exist_ok=True)
        with open(filepath, "a") as writer:
            writer.write(url_hash+"\n")
        return False
    else:
        raise RuntimeError(f"Unexpected grep return code: {res.returncode}|{res.stderr}")
