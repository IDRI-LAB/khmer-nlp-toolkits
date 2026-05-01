"""
Support func for text module.
"""
def unicode_escape(text: str):
    """
    Escape unicode.
    """
    unicode = []
    for char in text:
        unicode.append(f"\\u{ord(char):04X}")
    return "".join(unicode)
