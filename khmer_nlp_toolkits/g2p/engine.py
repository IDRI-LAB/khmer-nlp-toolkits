"""
Grapheme-to-Phoneme (G2P) module.

Convert Khmer words or text into phoneme sequences. The pronunciation models are Phonetisaurus
(OpenFst joint n-gram) models, available for three phoneme targets:

- ``ipa``: International Phonetic Alphabet.
- ``latin``: Latin-script phonetic spelling, readable without IPA knowledge.
- ``tts-v1``: A separate, richer label set (consonants/vowels plus pause and silence
  markers) matching one specific TTS front-end's convention. It is not a re-spelling of
  ``ipa``/``latin`` and is not guaranteed to match any other TTS system's phoneme set.

Inference is done in-process by `sosap <https://github.com/seanghay/sosap>`_, a pure-Rust Phonetisaurus
implementation with prebuilt wheels for Linux, macOS and Windows. ``sosap`` requires Python 3.11+, so
g2p is unavailable on Python 3.10 (a ``RuntimeError`` is raised when the models are first used).
"""
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Literal, Tuple, Union

import regex

from khmer_nlp_toolkits.number import num2text
from khmer_nlp_toolkits.text.segmentation import word_segment


__all__ = ["g2p", "g2p_word", "g2p_words", "TARGETS"]

TARGETS = ("ipa", "latin", "tts-v1")
MODEL_DIR = Path(__file__).parent / "model"

# Khmer consonants, independent/dependent vowels and signs. Excludes Khmer digits and punctuation.
_KHMER_WORD = regex.compile(r"^[\u1780-\u17D3\u17DD]+$")
_NUMBER = regex.compile(r"^[0-9\u17E0-\u17E9]+$")
_KHMER_DIGITS = str.maketrans("\u17E0\u17E1\u17E2\u17E3\u17E4\u17E5\u17E6\u17E7\u17E8\u17E9", "0123456789")

_CACHE_LIMIT = 50000
_CACHE: Dict[Tuple[str, str], List[str]] = {}


def _check_target(target: str) -> str:
    if target not in TARGETS:
        raise ValueError(f"target must be one of {TARGETS}. Given {target!r}.")
    return target


def _model_path(target: str) -> Path:
    path = MODEL_DIR / f"{target}.fst"
    if not path.is_file():
        raise FileNotFoundError(f"G2P model not found: {path}")
    return path


@lru_cache(maxsize=None)
def _load_model(target: str):
    """
    Load (once) the Phonetisaurus model of a target. ``sosap`` is imported lazily because it is
    only installed on Python 3.11+.
    """
    try:
        from sosap import Model  # pylint: disable=C0415
    except ImportError as err:
        raise RuntimeError(
            "g2p requires the `sosap` package, which needs Python 3.11 or newer. "
            "Install it with `pip install sosap`."
        ) from err
    return Model(str(_model_path(target)))


def _predict(words: List[str], target: str) -> Dict[str, List[str]]:
    """
    Decode a batch of words with the model of the target.

    Return
    ======
    Dict[str, List[str]]
        Mapping from word to its best phoneme sequence. Empty phoneme symbols are dropped.
    """
    model = _load_model(target)
    return {word: [phoneme for phoneme in model.phoneticize(word) if phoneme] for word in words}


def g2p_words(words: List[str], target: Literal["ipa", "latin", "tts-v1"] = "ipa") -> List[List[str]]:
    """
    Convert a batch of Khmer words to phonemes. Duplicate words are decoded once
    and results are cached.

    Parameters
    ==========
    words: List[str]
        Khmer words. Each word must not contain whitespace.
    target: Literal["ipa", "latin", "tts-v1"], default = "ipa"
        Phoneme target.

    Return
    ======
    List[List[str]]
        Phoneme sequence per word, in the same order as ``words``. Empty list for words that
        are not made of Khmer letters (e.g. digits or punctuation).
    """
    _check_target(target)
    if not isinstance(words, (list, tuple)):
        raise TypeError("words must be a list of str.")

    todo = sorted({w for w in words if _KHMER_WORD.match(w) and (w, target) not in _CACHE})
    if todo:
        if len(_CACHE) + len(todo) > _CACHE_LIMIT:
            _CACHE.clear()
        predictions = _predict(todo, target)
        for word in todo:
            _CACHE[(word, target)] = predictions.get(word, [])

    return [list(_CACHE.get((w, target), [])) for w in words]


def g2p_word(word: str, target: Literal["ipa", "latin", "tts-v1"] = "ipa") -> List[str]:
    """
    Convert one Khmer word to phonemes.

    Parameters
    ==========
    word: str
        A Khmer word.
    target: Literal["ipa", "latin", "tts-v1"], default = "ipa"
        Phoneme target.

    Return
    ======
    List[str]
        Phoneme sequence. Example: "ខ្មែរ" => ['kʰ', 'm', 'aɛ'] (ipa)
    """
    if not isinstance(word, str):
        raise TypeError("word must be str.")
    return g2p_words([word], target)[0]


def _tokenize(text: str, expand_numbers: bool) -> List[str]:
    tokens = []
    for token in word_segment(text, rt_type="list"):
        if expand_numbers and _NUMBER.match(token):
            tokens.extend(num2text(int(token.translate(_KHMER_DIGITS)), is_split=True))
        else:
            tokens.append(token)
    return tokens


def g2p(
        text: str,
        target: Literal["ipa", "latin", "tts-v1"] = "ipa",
        rt_type: Literal["str", "list"] = "str",
        word_sep: str = " | ",
        expand_numbers: bool = False
) -> Union[str, List[Tuple[str, List[str]]]]:
    """
    Convert Khmer text to phonemes. The text is segmented into words first, then each Khmer word is
    converted. Non-Khmer tokens (Latin words, punctuation) are kept as they are.

    Parameters
    ==========
    text: str
        Input Khmer text.
    target: Literal["ipa", "latin", "tts-v1"], default = "ipa"
        Phoneme target.
    rt_type: Literal["str", "list"], default = "str"
        - 'str' return phonemes of a word joined by space and words joined by ``word_sep``.
        - 'list' return a list of (token, phonemes) pairs.
    word_sep: str, default = " | "
        Word boundary marker when ``rt_type`` is 'str'.
    expand_numbers: bool, default = False
        Read numbers as Khmer words before conversion, e.g. "១២" => "ដប់ពីរ".

    Return
    ======
    Union[str, List[Tuple[str, List[str]]]]
        Phonemes of the text.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str.")
    if rt_type not in ("str", "list"):
        raise ValueError("rt_type must be 'str' or 'list'.")
    _check_target(target)

    tokens = _tokenize(text, expand_numbers)
    phonemes = g2p_words(tokens, target)
    # Tokens without phonemes (Latin words, punctuation) stay as-is.
    pairs = [(tok, ph if ph else [tok]) for tok, ph in zip(tokens, phonemes)]

    if rt_type == "list":
        return pairs
    return word_sep.join(" ".join(ph) for _, ph in pairs)
