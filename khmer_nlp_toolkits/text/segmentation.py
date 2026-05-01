"""
Segmentation module.
"""
import re
from typing import List, Literal

from khmernltk import word_tokenize

from khmer_nlp_toolkits.utils.keywords import SENTENCE_SEPARATOR
from khmer_nlp_toolkits.utils.segment.tokenizer import Tokenizer


PATTERN = r"(?<=[{}])\s*|(?=\b\d{{1,3}} ?[\)\.][^\S])".format("".join(SENTENCE_SEPARATOR))
tokenizer = Tokenizer("khmer_nlp_toolkits/utils/segment/model/morpheme_model.bin")


def sentence_segment(text: str) -> List[str]:
    """Khmer language sentence segmentation

    Parameters
    ==========
        text (str): Raw text

    Return
    ======
        List[str]: List of sentences
    """
    sentences = re.split(PATTERN, text)
    if "" in sentences:
        return [sent for sent in sentences if sent]
    return sentences


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
    paragraphs = re.split("៕", text)
    if "" in paragraphs:
        return [para for para in paragraphs if para]
    return paragraphs


def word_segment(text: str, word_type: Literal["com", "mor"] = "com"):
    """
    word tokenizer function called.
    """
    # Could be from khmer-nltk (remove log from khmernltk)
    # Or cadt-segment (download and keep in segment dir in first level of project)
    if word_type == "mor":
        return tokenizer.tokenize(text)
    words = word_tokenize(text)
    return " ".join(word for word in words if word != " ")
