import re


REPLACE_URL = re.compile(
    r'http\S+|www\.\S+|\b(?:[a-zA-Z0-9-]+\.)+'  # scheme or www. with subdomains and domain
    r'[A-Za-z]{2,}(?::\d+)?'                    # TLD (2+ chars) + optional port
    r'(?:/[A-Za-z0-9\-._~:/?#@!$&*+,;=%]*)?',   # optional path/query/fragment
    re.IGNORECASE
)


def run(text, url="[URL]"):
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


def replace_url(text: str, replace: str = "[URL]"):
    """
    Replace any link in string with the placeholder. if the placeholder not provided, the url
    will be replace with empty string.
    """
    return REPLACE_URL.sub(replace, text)


def replace_tel(text: str, replace: str = "[TEL]"):
    pass

def replace_email(text: str, replace: str = "[EMAIL]"):
    pass