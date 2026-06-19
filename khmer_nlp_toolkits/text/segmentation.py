"""
Segmentation module.
"""
import re
import logging
from pathlib import Path
from typing import List, Literal, Union
from functools import lru_cache

from khmernltk import word_tokenize

from khmer_nlp_toolkits.utils.keywords import SENTENCE_SEPARATOR
from khmer_nlp_toolkits.utils.segment.tokenizer import Tokenizer
from khmer_nlp_toolkits.utils.segment.kcc_split import seg_kcc


logging.getLogger("khmer-nltk").setLevel(logging.ERROR)


__all__ = [
    "sentence_segment",
    "paragraph_segment",
    "word_segment",
    "kcc_segment"
]


# This version split with number listing: ex: 1. 1) 12. however had problem with (2) => (\n2)
# PATTERN = r"(?<=[{}])\s*|(?=\b\d{{1,3}} ?[\)\.][^\S])".format("".join(SENTENCE_SEPARATOR))
PATTERN = r"(?<=[{}])\s*".format("".join(SENTENCE_SEPARATOR))
MORPHEM_MODEL_PATH = "khmer_nlp_toolkits/utils/segment/model/morpheme_model.bin"


@lru_cache(maxsize=1)
def _load_tokenizer():
    return Tokenizer(Path(__file__).parent.parent.parent.joinpath(MORPHEM_MODEL_PATH))


def sentence_segment(text: str) -> List[str]:
    """
    Khmer language sentence segmentation

    Parameters
    ==========
        text (str): Raw text

    Return
    ======
        List[str]: List of sentences
    """
    sentences = re.split(PATTERN, text)
    return [sent.strip() for sent in sentences if sent]


def paragraph_segment(text: str) -> List[str]:
    """
    Khmer language paragraphs segmentation.

    Parameters
    ==========
    text (str): Raw text

    Return
    ======
        List[str]: List of paragraph

    Notes
    =====
    In writing system of khmer language, ៕ use for paragraph ending.
    However, it is mostly use in NEWS article or Formal writing only.
    """
    paragraphs = re.findall(r"[^៕]+៕?", text)
    if "" in paragraphs:
        return [para for para in paragraphs if para]
    return paragraphs


def word_segment(
        text: str,
        word_type: Literal["com", "mor"] = "com",
        rt_type: Literal["str", 'list'] = "str"
) -> Union[str, list]:
    """
    word tokenizer function called.

    Parameters
    ==========
    text: str
        Input text.
    word_type: enum[str], default = 'com'
        Segmentation type.
        - 'com' stand for Compound word level.
        - 'mor' stand for Morpheme word level.
    rt_type: enum[str], default = 'str'
        Output format to given.
        - 'str' will return a sentence with space as word boundary.
        - 'list' will return list of word unit.

    Return
    ======
    Union[str, list]
        - String of sentence with space as word boundary.
        - List of string as a word unit.
    """
    if word_type not in ["com", "mor"]:
        raise ValueError("The word type must be 'com' or 'mor'.")
    if rt_type not in ["str", "list"]:
        raise ValueError("The word type must be 'str' or 'list'.")

    if word_type == "mor":
        res = _load_tokenizer().tokenize(text)
        if rt_type == "list":
            return res.split(" ")
        return res
    words = word_tokenize(text)
    res = [word for word in words if word != " "]
    if rt_type == "list":
        return res
    return " ".join(res)


def kcc_segment(text: str):
    """
    Khmer Character Clustering (KCC) segmentation.
    Example: "ភ្នំពេញ ថ្ងៃទី១៩ ខែមករា" => ['ភ្នំ', 'ពេ', 'ញ', 'ថ្ងៃ', 'ទី', '១៩', 'ខែ', 'ម', 'ក', 'រា']
    """
    if not isinstance(text, str):
        raise TypeError("text must be str.")

    return seg_kcc(text)
