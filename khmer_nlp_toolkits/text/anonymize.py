import re
from khmer_nlp_toolkits.text.clean import remove_invisible_chars


URL_PATTERN = re.compile(
    r'http\S+|www\.\S+|\b(?:[a-zA-Z0-9-]+\.)+'  # scheme or www. with subdomains and domain
    r'[A-Za-z]{2,}(?::\d+)?'                    # TLD (2+ chars) + optional port
    r'(?:/[A-Za-z0-9\-._~:/?#@!$&*+,;=%]*)?',   # optional path/query/fragment
    re.IGNORECASE
)
EMAIL_PATTERN = re.compile(r'[A-Za-z0-9\.\_\%\+\-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
TEL_PATTERN = re.compile(r"(\+[\d \-]{8,20}\d)|(0[0-9 \-]{7, 20}\d)")



def anonymizer(text: str):
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
    text = remove_invisible_chars(text)
    text = replace_email(text)  # must be email before url
    text = replace_url(text)
    text = replace_tel(text)
    # PII Removal
    return text


def replace_url(text: str, replace: str = "[URL]"):
    """
    Replace any link in string with the placeholder. if the placeholder not provided, the url
    will be replace with empty string.
    """
    return URL_PATTERN.sub(f" {replace} ", text)


def replace_tel(text: str, replace: str = "[TEL]"):
    return TEL_PATTERN.sub(f" {replace} ", text)



def replace_email(text: str, replace: str = "[EML]"):
    return EMAIL_PATTERN.sub(f" {replace} ", text)


if __name__ == "__main__":
    text = "hi sdf.sok.sao@eic2.edue2.kh, howe acer@ag.m jsldf"
    # text = "sok.sao@gmail.com "
    print(replace_email(text))
