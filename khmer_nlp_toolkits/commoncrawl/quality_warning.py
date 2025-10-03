import regex


def is_tiny(context: str):
    """
    Check if the context less than 5 sentences.
    """
    if not isinstance(context, str):
        raise TypeError("context must be a str.")
    return True if len(context.split("\n")) < 5 else False


def is_noisy(context: str):
    """
    Check if the context contain proportion of Khmer character compare to overall character
    is smaller than 0.5 ratio then it identifies as noisy.
    """
    if not isinstance(context, str):
        raise TypeError("context must be a str.")
    return True if len(regex.findall(r"\p{khmer}", context))/len(context) < 0.5 else False


def is_short_sentences(context: str):
    """
    Check if the context contain more short sentences (less than 75 character lenght)
    that exceed 0.5 ratio compare to total sentences.
    """
    if not isinstance(context, str):
        raise TypeError("context must be a str.")
    count = 0
    sentences = context.split("\n")
    for sentence in sentences:
        count += 1 if len(sentence) < 75 else 0
    return True if count/len(sentences) > 0.5 else False


def check_quality_warning(context: str):
    """
    Get all quality warning from the context.
    """
    if not isinstance(context, str):
        raise TypeError("context must be a str.")
    if not len(context):
        None
    result = []
    if is_tiny(context): result.append("tiny")
    if is_noisy(context): result.append("noisy")
    if is_short_sentences(context): result.append("short_sentences")
    return result if result else None
