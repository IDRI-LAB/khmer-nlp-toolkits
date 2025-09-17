"""
Module for text cleaning.
"""
import re
import regex
from unicodedata import category
from khmer_nlp_toolkits.keywords import INVISIBLE_CHARS
from khmer_nlp_toolkits.text.khnormal import khnormal


REPETITIVE_WHITESPACE = re.compile(r"[\s\u200b]{2,}")
SPACE_BETWEEN_KM = regex.compile(r'([\p{Script=Khmer}]+)')
SPACE_AFTER_PUNC = re.compile(r"([៖។៕.,!?;:\}\]\)]+)")
VARIATION_SELECTORS = re.compile(r'[\uFE00-\uFE0F]')
INV_CHARS = re.compile(rf"{'|'.join(INVISIBLE_CHARS)}")


def run(texts: list[str]) -> list[str]:
    """
    Main feature to clean text.

    Parameter
    ==========
    texts: List[str]
        List of string

    Return
    =======
    list of string
    """
    final_clean = []
    for text in texts:
        text = remove_repetitive_punc(text)
        # feature clean.enclosing_symbol_consistency
        text = remove_misc_symbols(text)
        text = space_handler(text)
        text = remove_invisible_chars(text)
        text = khnormal(text)
        final_clean.append(text)
    return final_clean


def remove_invisible_chars(text: str):
    """
    Remove 29 invisible character from the text.
    """
    return re.sub(INV_CHARS, "", text)


def space_handler(text: str):
    """
    Handle space cleaning and manipulation for khmer text.
    """
    text = text.replace("\u200b", "")
    text = __space_after_punc(text, clean=False)
    text = __space_between_km(text, clean=False)
    text = __remove_repitive_whitespace(text)
    text = __kh_strip(text)
    return text


def __kh_strip(text: str):
    """
    Custom strip to remove include \u200b. Normal strip function are not consider \u200b in their function.
    """
    return text.strip(" \t\n\r\v\f\u200b")


def __remove_repitive_whitespace(text: str):
    """
    Remove any repetitive space with just one space.
    """
    return REPETITIVE_WHITESPACE.sub(" ", text)


def __space_between_km(text: str, clean: bool = True):
    """
    Add space between khmer and other language.
    """
    if not clean:
        return SPACE_BETWEEN_KM.sub(r" \1 ", text)
    return SPACE_BETWEEN_KM.sub(r" \1 ", text).replace("  ", " ").strip()


def __space_after_punc(text: str, clean: bool = True):
    """
    Add space after punctuation if there aren't exist any whitespace after it.
    """
    # Can not check look ahead with regex, so use replace to work around instead.
    if not clean:
        return SPACE_AFTER_PUNC.sub(r"\1 ", text)
    return SPACE_AFTER_PUNC.sub(r"\1 ", text).replace("  ", " ").strip()


def remove_misc_symbols(text: str):
    """
    This function will remove any miscellaneous symbols (monochrome emoji and colorful emoji)
    that are classify by unicodedata (So). Unicodedata category symbol character into 4 types
    such as Math (Sm), Currency (Sc), Modifier (Sk), other (So).

    Return
    ------
    str
        String without emoji and symbol emoji.
    """
    if not isinstance(text, str):
        raise TypeError("Accept only string.")
    text = VARIATION_SELECTORS.sub("", text)
    text = [char for char in text if category(char) != "So"]
    return __kh_strip("".join(text))


def remove_repetitive_punc(text: str):
    """
    Replace consecutive mixed punctuation with only one occurrence of each.
    """
    # First, we find groups of punctuation and replace them.
    text = re.sub(r'([!?.,:;])\1+', r'\1', text)  # Collapse repeated punctuation (e.g., !!! becomes !)
    # Then, remove extra punctuation if there are multiple distinct ones
    text = re.sub(r'([!?.,:;])\1*([!?.,:;])\1*', r'\1\2', text)  # Keep only one of each mixed punctuation
    return text
