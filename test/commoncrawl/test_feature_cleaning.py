
from src.commoncrawl.feature_cleaning import filter_kh_lng
import pytest


"""
    clean text data and remove sentences that are not in Khmer
"""


@pytest.mark.parametrize('exp_input, exp_output', [
    (
        [
            " លោក តាន់ ហ្សង់ហ្វ្រង់ស្វ័រ៖ (Video inside)\nSearch ...\nFRESH NEWS+ English Chinese (中文)\nលោក តាន់\n2024-06-19 07:08pm",
            [
                {'label': 'km', 'prob': 0.99024457}, {'label': 'En', 'prob': 0.923842}, None, {
                    'label': 'km', 'prob': 0.99024457}, None
            ]
        ],
        [
            ' លោក តាន់ ហ្សង់ហ្វ្រង់ស្វ័រ៖ (Video inside)',
            'លោក តាន់',
        ]
    )
]
)
def test_filter_data(exp_input, exp_output):
    output = filter_kh_lng(*exp_input)
    assert output == exp_output
