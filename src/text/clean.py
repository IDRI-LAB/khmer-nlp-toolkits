"""
Module for text cleaning.
"""
import re
import regex


# def remove_repetitive_punc(text: str):
#     pass

# def remove_emoji(text: str):
#     pass

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


REPETITIVE_WHITESPACE = re.compile(r"[\s\u200b]{2,}")
def __remove_repitive_whitespace(text: str):
    """
    Remove any repetitive space with just one space.
    """
    return REPETITIVE_WHITESPACE.sub(" ", text)

SPACE_BETWEEN_KM = regex.compile(r'([\p{Script=Khmer}]+)') 
def __space_between_km(text:str, clean:bool=True):
    """
    Add space between khmer and other language.
    """
    if not clean:
        return SPACE_BETWEEN_KM.sub(r" \1 ", text)
    return SPACE_BETWEEN_KM.sub(r" \1 ", text).replace("  ", " ").strip()

SPACE_AFTER_PUNC = re.compile(r"([៖។៕.,!?;:\}\]\)]+)")
def __space_after_punc(text: str, clean:bool=True):
    """
    Add space after punctuation if there aren't exist any whitespace after it.
    """
    # Can not check look ahead with regex, so use replace to work around instead.
    if not clean:
        return SPACE_AFTER_PUNC.sub(r"\1 ", text)
    return SPACE_AFTER_PUNC.sub(r"\1 ", text).replace("  ", " ").strip()

