"""
Web crawling context quality checking.
"""
import regex


__all__ = ["check_quality_warning"]


def _is_tiny(context_line: list[str]):
    """
    Check if the context less than 5 sentences.
    """
    if not isinstance(context_line, list):
        raise TypeError("context must be a list[str].")
    return len(context_line) < 5


def _is_noisy(context: str):
    """
    Check if the context contain proportion of Khmer character compare to overall character
    is smaller than 0.5 ratio then it identifies as noisy.
    """
    if not isinstance(context, str):
        raise TypeError("context must be a str.")
    return len(regex.findall(r"\p{khmer}", context))/len(context) < 0.5


def _is_short_sentences(context_line: list[str]):
    """
    Check if the context contain more short sentences (less than 100 character lenght)
    that exceed 0.5 ratio compare to total sentences.
    """
    if not isinstance(context_line, list):
        raise TypeError("context must be a str.")
    count = 0
    for sentence in context_line:
        count += 1 if len(sentence) < 100 else 0
    return count/len(context_line) >= 0.5


def _is_header(context_line: list[str]):
    """
    Check if the top 20% lines of document are short_sentence,
    then annotate it as header.
    """
    if not isinstance(context_line, list):
        raise TypeError("context_line must be a list[str].")

    bound = int(len(context_line) * 0.2) + 1
    return _is_short_sentences(context_line[:bound])


def _is_footer(context_line: list[str]):
    """
    Check if the bottom 20% lines of document are short_sentence,
    then annotate it as footer.
    """
    if not isinstance(context_line, list):
        raise TypeError("context_line must be a list[str].")

    bound = int(len(context_line) * 0.2) + 1
    return _is_short_sentences(context_line[-bound:])


WARNING_FLAGSET = {
    "tiny": _is_tiny,
    "noisy": _is_noisy,
    "header": _is_header,
    "footer": _is_footer,
    "short_sentences": _is_short_sentences
}


def check_quality_warning(context: str):
    """
    Get all quality warning from the context.

    Parameters
    ==========
    context: str
        Text for check.

    Return
    ======
    list
        List of warning flags.

    Noted
    =====
    - noisy: Ratio of Khmer_char/total_char > 0.5
    - tiny: Contain less than or equal to 5 lines
    - short_sentence: count of line with less then 100 char/total lines > 0.5
    - header: top 20% of lines are short_sentence
    - footer: bottom 20% of lines is short_sentence
    """
    if not isinstance(context, str):
        raise TypeError("context must be a str.")
    if not context:
        raise ValueError("String is empty.")

    lines = context.split("\n")

    result = []
    for flag, flag_func in WARNING_FLAGSET.items():
        if flag == "noisy":
            if flag_func(context):
                result.append(flag)
            continue
        if flag_func(lines):
            result.append(flag)

    return result
