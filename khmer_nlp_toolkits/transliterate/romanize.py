"""
Romanizer module.

This module was provided a transliterater function from khmer to roman.
"""
import pickle
from functools import lru_cache
from typing import Union


__all__ = ["romanizer"]
MODEL_PATH = "khmer_nlp_toolkits/transliterate/model/romanize_model.bin"


def _preprocess(name):
    """
    Preprcess of romanizer before feed to model prediction.
    """
    sample = []
    for idx, char in enumerate(name):
        if char == ' ':
            sample.append('_')
            continue

        sample.append(char)

        next_char = name[idx + 1] if idx < len(name) - 1 else char
        if 6016 <= ord(char) <= 6050:
            if 6016 <= ord(next_char) <= 6050 or next_char == ' ':
                sample.append('@')

    return _name2features(sample)


def _postprocess(name):
    """
    Postprocess of romanizer model prediction.
    """
    result = ''
    for char in name:
        if char == '@':
            continue
        if char == '_':
            result += ' '
        else:
            result += char
    return result


def _char2features(name, i):
    """
    Feature extraction on char gram.
    """
    char = name[i][0]

    features = {
        'char': char,
    }

    # char[-3]
    if i > 2:
        features.update({
            'char[-3]': name[i - 3][0],
            'char[-3:-2]': name[i - 3][0] + name[i - 2][0],
            'char[-3:-1]': name[i - 3][0] + name[i - 2][0] + name[i - 1][0],
            'char[-3:0]': name[i - 3][0] + name[i - 2][0] + name[i - 1][0] + name[i][0]
        })

    # char[-2]
    if i > 1:
        features.update({
            'char[-2]': name[i - 2][0],
            'char[-2:-1]': name[i - 2][0] + name[i - 1][0],
            'char[-2:0]': name[i - 2][0] + name[i - 1][0] + name[i][0]
        })

    # char[-1]
    if i > 0:
        features.update({
            'char[-1]': name[i - 1][0],
            'char[-1:0]': name[i - 1][0] + name[i][0]
        })
    else:
        features['BOS'] = True

    # char[+1]
    if i < len(name) - 1:
        features.update({
            'char[+1]': name[i + 1][0],
            'char[0:+1]': name[i][0] + name[i + 1][0]
        })
    else:
        features['EOS'] = True

    # char[+2]
    if i < len(name) - 2:
        features.update({
            'char[+2]': name[i + 2][0],
            'char[+1:+2]': name[i + 1][0] + name[i + 2][0],
            'char[0:+2]': name[i][0] + name[i + 1][0] + name[i + 2][0]
        })

    # char[+3]
    if i < len(name) - 3:
        features.update({
            'char[+3]': name[i + 3][0],
            'char[+2:+3]': name[i + 2][0] + name[i + 3][0],
            'char[+1:+3]': name[i + 1][0] + name[i + 2][0] + name[i + 3][0],
            'char[0:+3]': name[i][0] + name[i + 1][0] + name[i + 2][0] + name[i + 3][0]
        })

    return features


def _name2features(name):
    """
    name feature extraction.
    """
    return [_char2features(name, i) for i in range(len(name))]


@lru_cache(maxsize=1)
def _load_romanizer_model():
    """
    Load romanizer model with cache to load one time only
    and the next called will be reuse the cache.
    """
    with open(MODEL_PATH, "rb") as model:
        model = pickle.load(model)
    return model
    # return Romanizer(MODEL_PATH)


def romanizer(names: Union[str, list[str]]) -> Union[str, list[str]]:
    """
    Romanizer function.

    Parameters
    ==========
    names: Union[str, list[str]]
        String of name or list of names.

    Return
    ======
    Union[str, list[str]]
        String of romanized name or list of romanized names.
    """
    model = _load_romanizer_model()
    if isinstance(names, str):
        names = [names]

    names = [_preprocess(n) for n in names]
    latins = model.predict(names)
    latins = [_postprocess(n) for n in latins]
    return latins if len(latins) > 1 else latins[0]
