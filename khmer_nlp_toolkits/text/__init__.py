"""
Support func for text module.
"""
# flake8: noqa: F401,F403
import regex

from khmer_nlp_toolkits.text.anonymize import *
from khmer_nlp_toolkits.text.normalize import *
from khmer_nlp_toolkits.text.clean import *
from khmer_nlp_toolkits.text.segmentation import *
from khmer_nlp_toolkits.text.mask_lang import lang_masking


def unicode_escape(text: str):
    """
    Escape unicode.
    """
    unicode = []
    for char in text:
        unicode.append(f"\\u{ord(char):04X}")
    return "".join(unicode)


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
