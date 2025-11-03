import regex


EN_RANGE = r"\u0000-\u00bb"
KM_RANGE = r"\u1780-\u17FF"
GREEK_RANGE = r"\u0370-\u03FF"
MASK = regex.compile(rf"[^\p{{S}}{EN_RANGE}{KM_RANGE}{GREEK_RANGE}]+")


def masking(obj):
    if not obj:
        return None
    obj["content"] = MASK.sub("[UNK]", obj["content"])
    return obj
