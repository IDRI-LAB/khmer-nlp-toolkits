"""
Module for text normalization.
"""
from unicodedata import normalize
from khmer_nlp_toolkits.utils.khnormal import khnormal


def nomalizer(text: str) -> list[str]:
    """
    Main feature to clean text.

    Parameter
    ==========
    texts: str
        String of text to be clean.

    Return
    ======
        String of text after cleanning.
    """
    text = normalize("NFKD", text).lower()
    text = khnormal(text)
    return text
