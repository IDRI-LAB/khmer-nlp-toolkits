"""
Module for test feature cleaning on commoncrawl data structure.
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from khmer_nlp_toolkits.commoncrawl import feature_cleaning as fc


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
            "លោក តាន់ ហ្វ្រង់ស្វ័រ៖ (Video inside)",
            "លោក តាន់",
        ]
    )
])
def test_filter_data_equal_len(exp_input, exp_output):
    """
    clean text data and remove sentences that are not in Khmer
    """
    output = fc.filter_kh_lng(*exp_input)
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
        fc.filter_kh_lng(*exp_input)


@pytest.mark.parametrize("exp_qua_input, exp_qua_output", [
    (
        [[
            "ករណីទន្ទ្រានកាន់កាប់ដីព្រៃលិចទឹក",
            "សុខភាព",
            "លោកស្រី Peng Liyuan ជួបជាមួយលោកស្រី Iriana ភរិយាប្រធានាធិបតីឥណ្ឌូណេស៊ី",
            " (ផ្សាយឡើងវិញ) គោលនយោបាយ BRI បានរុញ ឡាវនិងកម្ពុជា ចេញផុតពីតារាវិថី នៃអំណាចឥទ្ធិពល របស់វៀតណាម",
            "ព័ត៌មានជាតិ",
            "អ៊ីរ៉ង់ កំពុងស្វែងរក​ការ​សងសឹក ចំពោះ​ការ​762467177777724713741873478123431876412434",
            "តេអេរ៉ង់៖ អ៊ីរ៉ង់នឹងស្វែងរកការសងសឹក ចំពោះការចោទប្រកាន់របស់អ៊ីស្រាអែលថា ការធ្វើឃាតប្រធានការិយាល័យ នយោបាយ",
        ], ["short_sentences", "header", "noisy"]],
        [
            " (ផ្សាយឡើងវិញ) គោលនយោបាយ BRI បានរុញ ឡាវនិងកម្ពុជា ចេញផុតពីតារាវិថី នៃអំណាចឥទ្ធិពល របស់វៀតណាម",
            "តេអេរ៉ង់៖ អ៊ីរ៉ង់នឹងស្វែងរកការសងសឹក ចំពោះការចោទប្រកាន់របស់អ៊ីស្រាអែលថា ការធ្វើឃាតប្រធានការិយាល័យ នយោបាយ",
        ]
    ),
    (
        [[
            "(ផ្សាយឡើងវិញ) គោលនយោបាយ BRI បានរុញ ឡាវនិងកម្ពុជា ចេញផុតពីតារាវិថី នៃអំណាចឥទ្ធិពល របស់វៀតណាម",
            "អ៊ីរ៉ង់ កំពុងស្វែងរក​ការ​សងសឹក ចំពោះ​ការ​762467177777724713741873478123431876412434",
            "តេអេរ៉ង់៖ អ៊ីរ៉ង់នឹងស្វែងរកការសងសឹក ចំពោះការចោទប្រកាន់របស់អ៊ីស្រាអែលថា ការធ្វើឃាតប្រធានការិយាល័យ នយោបាយ",
        ], ["noisy"]],
        [
            "(ផ្សាយឡើងវិញ) គោលនយោបាយ BRI បានរុញ ឡាវនិងកម្ពុជា ចេញផុតពីតារាវិថី នៃអំណាចឥទ្ធិពល របស់វៀតណាម",
            "តេអេរ៉ង់៖ អ៊ីរ៉ង់នឹងស្វែងរកការសងសឹក ចំពោះការចោទប្រកាន់របស់អ៊ីស្រាអែលថា ការធ្វើឃាតប្រធានការិយាល័យ នយោបាយ",
        ]
    ),
    (
        [[
            " (ផ្សាយឡើងវិញ) ​គោលនយោបាយ BRI បានរុញ ឡាវនិងកម្ពុជា ចេញផុតពីតារាវិថី នៃអំណាចឥទ្ធិពល របស់វៀតណាម",
            "តេអេរ៉ង់៖ អ៊ីរ៉ង់នឹងស្វែងរកការសងសឹក ចំពោះការចោទប្រកាន់របស់អ៊ីស្រាអែលថា ការធ្វើឃាតប្រធានការិយាល័យ នយោបាយ",
        ], None],
        [
            "(ផ្សាយឡើងវិញ) ​គោលនយោបាយ BRI បានរុញ ឡាវនិងកម្ពុជា ចេញផុតពីតារាវិថី នៃអំណាចឥទ្ធិពល របស់វៀតណាម",
            "តេអេរ៉ង់៖ អ៊ីរ៉ង់នឹងស្វែងរកការសងសឹក ចំពោះការចោទប្រកាន់របស់អ៊ីស្រាអែលថា ការធ្វើឃាតប្រធានការិយាល័យ នយោបាយ",
        ]
    ),
    (
        [[
            " ​​​​​​ ​​​​ ​​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​​ ​​ ​ "
        ], ["tiny", "noisy"]],
        []
    )
]
)
def test_check_quality_warning(exp_qua_input, exp_qua_output):
    """
    clean data by check quality warning
    """
    output = fc.check_quality_warning(*exp_qua_input)
    assert output == exp_qua_output


@pytest.mark.parametrize("exp_input, exp_output", [
    ("https://www.amloud.de/google-amp-slen.php?hl=km&s=https%3A%2F%2Fpornewap.com%2Ffuck-video%2Fmom-fucking-toy", True),
    ("https://km.phimsexnh.caa/category", True),
    ("https://bizkhmer.com/articles/18357", False),
    ("https://www.cambopay.com.kh/km-kh/%E1%9E%94%E1%9E%91%E1%9E%96%E1%9E%B7%E1%9E%9F%E1%9F", False)
])
def test_is_adult_url_filter(exp_input, exp_output):
    assert fc.is_adult_url_filter(exp_input) == exp_output


@pytest.mark.parametrize("exp_in, exp_ret, exp_out", [
    (["https://t.me", "dedup"], 0,  True),
    (["https://t.me", "dedup"], 1, False)
])
def test_is_url_duplicated(exp_in, exp_ret, exp_out):
    mock_res = MagicMock()
    mock_res.returncode = exp_ret
    with patch("subprocess.run", return_value=mock_res) as mock_run, \
        patch("builtins.open", mock_open()):
        assert fc.is_url_duplicated(*exp_in) == exp_out


@pytest.mark.parametrize("exp_in, exp_ret, exp_out", [
    (["https://t.me", "dedup"], 3, False)
])
def test_is_url_duplicated(exp_in, exp_ret, exp_out):
    mock_res = MagicMock()
    mock_res.returncode = exp_ret
    with patch("subprocess.run", return_value=mock_res) as mock_run, \
        patch("builtins.open", mock_open()):
        with pytest.raises(RuntimeError):
            fc.is_url_duplicated(*exp_in)
