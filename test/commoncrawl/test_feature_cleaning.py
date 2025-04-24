
from src.commoncrawl.feature_cleaning import filter_kh_lng
import pytest


"""
    clean text data and remove sentences that are not in Khmer
"""
@pytest.mark.parametrize('exp_input, exp_output', [
    (
        [
            "លោក តាន់ ហ្វ្រង់ស្វ័រ៖ (Video inside)\nSearch ...\nFRESH NEWS+ Chinese (中文)\nលោក តាន់\n2024-06-19 07:08pm",
            [
                {'label': 'km', 'prob': 0.99024457}, {'label': 'En', 'prob': 0.923842}, None, 
                {'label': 'km', 'prob': 0.99024457}, None
            ]
        ],
        [
            'លោក តាន់ ហ្វ្រង់ស្វ័រ៖ (Video inside)',
            'លោក តាន់',
        ]
    )
]
)
def test_filter_data_equal_len(exp_input, exp_output):
    output = filter_kh_lng(*exp_input)
    assert output == exp_output


@pytest.mark.parametrize('exp_input, exp_output', [
    (
        [
            "លោក តាន់ ហ្វ្រង់ស្វ័រ៖ (Video inside)\nSearch ...\nFRESH NEWS+ Chinese (中文)\nលោក តាន់\n2024-06-19 07:08pm",
            [
                {'label': 'km', 'prob': 0.99024457}, {'label': 'En', 'prob': 0.923842}, None, 
                {'label': 'km', 'prob': 0.99024457}, None, {'label': 'km', 'prob': 0.99024457}
            ]
        ],
        None
    )
]
)
def test_filter_data_unequal_len(exp_input, exp_output):
    with pytest.raises(ValueError, match="List is not in equal lenght"):
        filter_kh_lng(*exp_input)
