"""
Module for text cleaning.

# Thing solve by ftfy.fix_text
# remove few hidden space and Control Unicode
# all quote ' " ‘ ’ “ ” ‚ „ ‛ ‟ -> '" respectively, except ′ (prime) ″ (Double prime) using for unit or in math
"""
import re
from unicodedata import category

import regex
from ftfy import fix_text

from khmer_nlp_toolkits.utils.keywords import INVISIBLE_CHARS


REPETITIVE_WHITESPACE = re.compile(r"[\s\u200b]{2,}")
SPACE_BETWEEN_KM = regex.compile(r'([\p{Script=Khmer}\.\,0-9]{2,})')
SPACE_AFTER_PUNC = re.compile(r"([%៖។៕!?;:,#\.\-\_\/\\]+)")
VARIATION_SELECTORS = re.compile(r'[\uFE00-\uFE0F]')
INV_CHARS = re.compile(rf"{'|'.join(INVISIBLE_CHARS)}")
SPACE_AROUND_BRACKET = re.compile(r'([\(\)\[\]\{\}\<\>«»‹›])')
HANDLE_LINKING_WORD_NUM = re.compile(r"(?<![\-\_]) *([\-\_]) *(?![\-\_])")
SPACE_ARROUND_NUMBER = re.compile(r"(\d+([\.\,\-\_]?\d*)+)")
FILTER_CHAR_TYPE = [
    "Cf", "Cn", "Co", "Cs",
    "So", "Sk",
    "Mn", "Me", "Ms",
    "Lm"
]
# Basic latin + latin1-supplement, khmer, greek (for unit)
CHAR_INCLUDE = [(0x0020, 0x007E), (0x00A1, 0x00BB), (0x1780, 0x17FF), (0x0370, 0x03FF)]
EXCEPTION_SET = {chr(cp) for start, end in CHAR_INCLUDE for cp in range(start, end + 1)}


def text_cleaner(text: str) -> list[str]:
    """
    Main feature to clean text.

    Parameter
    =========
    texts: str
        String of text to be clean.

    Return
    ======
        String of text after cleanning.
    """
    text = remove_invisible_chars(text)
    text = replace_by_space(text)
    text = re.sub(r"[\u2010-\u2015]", "-", text)
    text = fix_text(text, normalization="NFKD")
    text = remove_misc_symbols(text)
    text = remove_repetitive_punc(text)
    text = add_space_around_bracket(text)
    text = space_handler(text)
    return text


def remove_invisible_chars(text: str):
    """
    Remove 29 invisible character from the text.
    """
    return re.sub(INV_CHARS, "", text)


def space_handler(text: str):
    """
    Handle space cleaning and manipulation for khmer text.
    """
    text = __space_after_punc(text, clean=False)
    text = __space_between_km(text, clean=False)
    text = __space_with_number(text)
    # text = __handle_linking_word_num(text)
    text = __remove_repitive_whitespace(text)
    text = __kh_strip(text)
    return text


def replace_by_space(text: str):
    """
    Replace \\s and &nbsp; to a space.
    """
    return re.sub(r"\s|&nbsp;", " ", text)


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
        return SPACE_AFTER_PUNC.sub(r" \1 ", text)
    return SPACE_AFTER_PUNC.sub(r" \1 ", text).replace("  ", " ").strip()


def __handle_linking_word_num(text: str):
    """
    It is handle only hypen and underscore.
    Ex: "123 _ 123" -> "123_123"
    Ex: "mother - in - law" -> "mother-in-law"
    But not "123 -- 123" !-> "123--123"
    """
    return HANDLE_LINKING_WORD_NUM.sub(r"\1", text)


def __space_with_number(text: str):
    text = SPACE_ARROUND_NUMBER.sub(r" \1 ", text)
    return text


def remove_misc_symbols(text: str):
    """
    This function will remove any miscellaneous symbols (monochrome emoji and colorful emoji)
    that are classify by unicodedata (So & Sk). Unicodedata categorize symbol character into 4 types
    such as Math (Sm), Currency (Sc), Modifier (Sk), other (So).

    Return
    ------
    text: str
        String without emoji and symbol emoji.
    exception: str
        Unicode character that will not remove.
        Usage: "abc" => character a, b, c will not remove.

    Noted
    -----
    In khmer character unicdoe range 1780-17FF (Khmer), There are no 'Sk'. And 19E0-19FF (Khmer Symbol) are 'So'.
    Character type: https://www.fileformat.info/info/unicode/category/index.htm
    """
    if not isinstance(text, str):
        raise TypeError("Accept only string.")
    text = VARIATION_SELECTORS.sub("", text)
    text = [char for char in text if char in EXCEPTION_SET or category(char) not in FILTER_CHAR_TYPE]
    return __kh_strip("".join(text))


def remove_repetitive_punc(text: str):
    """
    Replace consecutive mixed punctuation with only one occurrence of each.
    """
    # First, we find groups of punctuation and replace them.
    text = re.sub(r'([!?.,:;\_\-\=\*\'\"])\1+', r'\1', text)  # Collapse repeated punctuation (e.g., !!! becomes !)
    # Then, remove extra punctuation if there are multiple distinct ones
    # Keep only one of each mixed punctuation
    text = re.sub(r'([!?.,:;\_\-\=\*\'\"])\1*([!?.,:;\_\-\=\*\'\"])\1*', r'\1\2', text)
    return text


def add_space_around_bracket(text: str):
    """
    Add space around open and close bracket.
    """
    return SPACE_AROUND_BRACKET.sub(r" \1 ", text)


def count_khmer_char(sent: str):
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
    return len(regex.findall(r"\p{khmer}", sent))
