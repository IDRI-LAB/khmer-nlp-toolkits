import re


REPLACE_URL = re.compile(r'(http\S+|www\.\S+|\b(?:[a-zA-Z0-9-]+\.)+(com|org|net|edu|gov|io|co|info|tv|me|ai|app)(/\S*)?)')


def anonymize(text, url="[URL]"):
    """
    Main feature for anonymize data such as entity or identities.

    Parameters
    ==========
    text: str
        Text to process.
    url: str
        Placeholder to replace url string.

    Return
    ======
    str
        String after anonymize.
    """
    text = replace_url(text, url)
    # PII Removal
    return text


def replace_url(text: str, replace: str = ""):
    """
    Replace any link in string with the placeholder. if the placeholder not provided, the url
    will be replace with empty string.
    """
    return REPLACE_URL.sub(replace, text)
