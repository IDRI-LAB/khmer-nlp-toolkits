def unicode_escape(text: str):
    unicode = []
    for char in text:
        unicode.append(f"\\u{ord(char):04X}")
    return "".join(unicode)