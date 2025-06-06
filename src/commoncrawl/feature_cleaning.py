"""
Module for apply feature cleaning on commoncrawl data structure.
"""
from typing import Union, Optional, List, Dict
from src.text.clean import __kh_strip
import tlsh
from itertools import product

final_data = []


def cleaning_kh_data(data: Union[dict, list], threshold: int = 75) -> List[str]:
    """
        Cleaning all khmer data
        Parameter
        ==========
        data: Union[dict, list]
            List of json data for cleaning
        return
        =======
        khmer data
    """

    cleaned_sents = filter_kh_lng(data['content'], data['metadata']['sentence_identifications'])
    cleaned_sents = check_quality_warning(cleaned_sents, data['metadata']['quality_warnings'], threshold=threshold)
    cleaned_sents = remove_sentence_deduplicate(cleaned_sents)
    return cleaned_sents


def filter_kh_lng(contents: List[str], sent_idens: List[Optional[Dict[str, float]]]):
    """
        Filter data to get only the content with Khmer language label ("kh")
        and Identification data is not None.
        Parameters
        ==========
        contents: List[str]
                  content for cleaning
        sent_idens: List[Optional[Dict[str, float]]]
                   sentent identification to check label 'km'
        Return
        ======
        contents: List[str]
            list of content that has khmer language label 'km' and not None
        Noted
        =====
        - if content is None, it will be removed.
        - if content is not in Khmer language, it will be removed.
        - if content is not in equal length with sentence identification, it will be raise.

    """

    if not contents or not sent_idens:
        raise ValueError("Missing contents or sentence identifications")
    content_split = contents.split('\n')
    print(len(content_split), len(sent_idens))
    if len(content_split) != len(sent_idens):
        raise ValueError("List is not in equal lenght")
    list_data_kh = []
    for iden_data, con_data in zip(sent_idens, content_split):
        if iden_data is not None and iden_data['label'] == "km":
            list_data_kh.append(con_data)
    return list_data_kh


def check_quality_warning(sentences: List[str], qua_warning: List[str], threshold: int = 75):
    """
    check quality warninng data.

    Parameters
    ==========
    sentences: List[str]
        list of sentence for cleaning if it has quality warning
    qua_warning: List[str]
        list of quality warning
    threshold: int = 75
        threshold to filter sentence character length

    Return
    ======
    sentences: List[str]
        list of sentence for cleaning if it has quality warning

    Noted
    ======
    - if sentence has number char more than 50% of the sentence, it will be removed.
    - if sentence length is less than threshold, it will be removed.
    """

    def extract_numbers(sent: str):
        """
            extract sentence that has number char
            Parameters
            ==========
            sent: str
                sentence to get only number char
            EX: "សួស្ដី១២៣៤" -> "១២៣៤"
        """
        return ''.join(char for char in sent if char.isdigit())

    if sentences and qua_warning:
        return [
            __kh_strip(sent)
            for sent in sentences
            if len(sent) > threshold
            and len(extract_numbers(sent)) / len(sent) < 0.5
            and __kh_strip(sent) != ''
        ]
    return [__kh_strip(sent) for sent in sentences]


def remove_sentence_deduplicate(sentences: List[str], threshold: int = 100):
    """
        check duplicate sentence by tlsh value
        Parameters
        ==========
        sentences: List[str]
                   list of sentence for cleaning
        threshold: int = 100
                   threshold to compare with tlsh value
        Return
        ======
        sentences: List[str]
            list of sentence for cleaning if it has duplicate
        Noted   
        ======
        - if tlsh value is less than threshold, it will be removed.
        - if tlsh value is more than threshold, it will be added to final_data
    """
    def compute_tlsh_hash(text):
        # if len(text) <= 50:
        #     raise ValueError("Invalid TLSH hash")
        t = tlsh.Tlsh()
        t.update(text.encode('utf-8'))
        t.final()
        return t
    if len(final_data) == 0:
        final_data.extend(sentences)
    else:
        for (_, sentence), (i_data_comparing, data_comparing) in product(enumerate(sentences), enumerate(final_data)):
            tlsh_sentence = compute_tlsh_hash(sentence)
            tlsh2_data_comparing = compute_tlsh_hash(data_comparing)
            # if hash1 and hash2:
            score = tlsh_sentence.diff(data_comparing)
            if score <= threshold:
                break
            elif i_data_comparing == len(final_data) - 1:
                final_data.append(sentence)
    return final_data
