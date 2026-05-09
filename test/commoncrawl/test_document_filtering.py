"""
Module for test document filtering module.
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from khmer_nlp_toolkits.commoncrawl import document_filtering as df


@pytest.mark.parametrize("exp_input, exp_output", [
    ("https://www.amloud.de/google-amp-slen.php?hl=km&s=https%3A%2F%2Fpornewap.com%2Ffuck-video%2Fmom-fucking-toy", True),
    ("https://km.phimsexnh.caa/category", True),
    ("https://bizkhmer.com/articles/18357", False),
    ("https://www.cambopay.com.kh/km-kh/%E1%9E%94%E1%9E%91%E1%9E%96%E1%9E%B7%E1%9E%9F%E1%9F", False)
])
def test_is_adult_url_filter(exp_input, exp_output):
    assert df.is_adult_url_filter(exp_input) == exp_output


@pytest.mark.parametrize("exp_input, exp_output", [
    ([], "High"),
    (["tiny"], "High"),
    (["short_sentences"], "Low"),
    (["header"], "Medium"),
    (["footer"], "Medium"),
    (["noisy"], "Medium"),
    (["header", "footer"], "Medium"),
    (["header", "footer", "noisy"], "Medium"),
    (["footer", "tiny"], "Medium"),
    (["tiny", "noisy"], "Medium"),
    (["tiny", "short_sentences"], "Low")
])
def test_classify_doc_quality(exp_input, exp_output):
    assert df.classify_doc_quality(exp_input) == exp_output


def test_classify_doc_quality():
    with pytest.raises(TypeError, match="quality_warning must be list of string."):
        df.classify_doc_quality("tiny")
    with pytest.raises(
        ValueError,
        match="Got unexpected warning flags. See quality_warning for flag info."
    ):
        df.classify_doc_quality(["tinys"])
