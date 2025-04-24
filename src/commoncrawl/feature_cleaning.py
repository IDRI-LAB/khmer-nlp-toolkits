"""
Module for apply feature cleaning on commoncrawl data structure.
"""
from typing import Union, Optional, List, Dict


def cleaning_kh_data(data: Union[dict, list]):
    """
        Cleaning all khmer data
        Parameter
        ============
        data: Union[dict, list]
            List of json data for cleaning
        return
        ============
        khmer data
    """

    cleaned_sents = filter_kh_lng(data['content'], data['metadata']['sentence_identifications'])
    return cleaned_sents


def filter_kh_lng(contents: List[str], sent_idens: List[Optional[Dict[str, float]]]):
    """
        Filter data to get only the content with Khmer language label ("kh")
        and Identification data is not None.
        ===================
        contents: List[str]
                  content for cleaning
        sent_idens: List[Optional[Dict[str, float]]]
                   sentent identification to check label 'km'
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
