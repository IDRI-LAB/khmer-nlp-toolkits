"""
Module for text normalization.
"""
import re
from unicodedata import normalize
from khmer_nlp_toolkits.utils.khnormal import khnormal


SMART_QUOTES = re.compile(r"[‘’“”]")


def run(text: str) -> list[str]:
    """
    Main feature to clean text.

    Parameter
    ==========
    texts: str
        String of text to be clean.

    Return
    =======
        String of text after cleanning.
    """
    text = khnormal(text)
    text = normalize("NFKD", text)
    text = normalize_symbol(text)
    return text


def normalize_symbol(text: str):
    text = SMART_QUOTES.sub(lambda m: "'" if m.group() in "‘’" else '"', text)
    text = text.replace("\u2013", "\u002d")
    return text
