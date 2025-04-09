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

    cleaned_sentens = filter_kh_lng(data['content'], data['metadata']['sentence_identifications'])
    cleaned_sentens = check_quality_warning(cleaned_sentens, data['metadata']['quality_warnings'])
    return cleaned_sentens


def filter_kh_lng(contents, sent_idens):
    """
        Filter data to get only the content with Khmer language label ("kh")
        and Identification data is not None.
    """
    def extract_list_lng_identification(contents):
        """
            Extract content and language identification from the given data.
            ===============
            split '\n' in data of content and convert to list of content
            Return
            =======
            list of content and sentence_identifications
        """
        content_list = []
        if contents:
            content_split = contents.split('\n')
            content_list.append(content_split)
        else:
            print("No content found in entry.")
        return content_list
    list_data_kh = []
    for data in extract_list_lng_identification(contents):
        for iden_data, con_data in zip(sent_idens, data):
            if iden_data is not None:
                label = iden_data.get("label")
                if label == "km":
                    list_data_kh.append(con_data)
    return list_data_kh


def check_quality_warning(sentents, qua_warning):

    return
