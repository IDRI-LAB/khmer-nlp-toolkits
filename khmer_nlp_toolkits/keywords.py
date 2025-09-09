"""
This module is using to store any keyword for using over the project.
"""


# This is the keyword of inappropriate keyword appear might use in URI, and we use it to identity
# any adult content from website. Checkout function: khmer_nlp_toolkits.commoncrawl.feature_cleaning.py
ALDULT_KW = ["sex", "pornography", "porn", "xxx", "adult", "erotic", "intimate", "nude", "nudity", "boob", "breasts", "vagina", "penis", "intercourse", "masturbation", "fetish", "orgy", "hardcore", "deepthroat", "blowjob", "gangbang", "strip", "lap dance", "pornographic", "bondage", "bdsm", "tits", "cock", "dick", "pussy", "cleavage", "adult films", "adult movies", "adult video", "adult website", "escort", "masseuse", "strip club", "brothel", "sex shop", "18+", "18plus"]  # noqa: E501  # pylint: disable=C0301

# This is reference from “Table 11: List of invisible characters to remove.” ([Hour et al., 2025, p. 1321]
# Ref: https://aclanthology.org/2025.coling-main.87/
INVISIBLE_CHARS = [
    "\u2063",  # INVISIBLE SEPARATOR
    "\u202A",  # LEFT-TO-RIGHT EMBEDDING
    "\u200C",  # ZERO WIDTH NON-JOINER
    "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE
    "\u202C",  # POP DIRECTIONAL FORMATTING
    "\u200F",  # RIGHT-TO-LEFT MARK
    "\uFE0E",  # VARIATION SELECTOR-15 (text style)
    "\uFE0F",  # VARIATION SELECTOR-16 (emoji style)
    "\u00AD",    # SOFT HYPHEN
    "\u202D",  # LEFT-TO-RIGHT OVERRIDE
    "\u180C",  # MONGOLIAN FREE VARIATION SELECTOR-2
    "\u200E",  # LEFT-TO-RIGHT MARK
    "\u180B",  # MONGOLIAN FREE VARIATION SELECTOR-1
    "\u206E",  # NOMINAL DIGIT SHAPES
    "\u200B",  # ZERO WIDTH SPACE
    "\u180D",  # MONGOLIAN FREE VARIATION SELECTOR-3
    "\u202B",  # RIGHT-TO-LEFT EMBEDDING
    "\u2060",  # WORD JOINER
    "\u17B5",  # KHMER VOWEL SIGN AA
    "\u17B4",  # KHMER VOWEL SIGN I
    "\u200D",  # ZERO WIDTH JOINER
    "\u180E",  # MONGOLIAN VOWEL SEPARATOR
    "\u2061",   # FUNCTION APPLICATION
    "\U000E007F",  # CANCEL TAG
    "\U000E0067",  # TAG LETTER G
    "\U000E0065",  # TAG LETTER E
    "\U000E01D3",  # (Private use / specific tag)
    "\U000E0062",  # TAG LETTER B
    "\U000E006E",  # TAG LETTER N
]
