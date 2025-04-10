"""
Module for apply feature cleaning on commoncrawl data structure.
"""
from typing import Union


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
    cleaned_sents = check_quality_warning(cleaned_sents, data['metadata']['quality_warnings'])
    return cleaned_sents


def filter_kh_lng(contents, sent_idens):
    """
        Filter data to get only the content with Khmer language label ("kh")
        and Identification data is not None.
    """
    if contents:
        content_split = contents.split('\n')

    list_data_kh = []
    for iden_data, con_data in zip(sent_idens, content_split):
        if iden_data is not None and iden_data['label'] == "km":
            list_data_kh.append(con_data)
    return list_data_kh


def check_quality_warning(sentents, qua_warning):

    return
