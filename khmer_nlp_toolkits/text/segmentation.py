import re
from typing import List
from khmer_nlp_toolkits.utils.keywords import SENTENCE_SEPARATOR


PATTERN = r"(?<=[{}])\s*|(?=\d+ ?[\)\.][^\S])".format("".join(SENTENCE_SEPARATOR))


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
