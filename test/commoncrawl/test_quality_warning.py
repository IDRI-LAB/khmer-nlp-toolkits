"""
Module for test quality warning function.
"""
from pathlib import Path

import pytest
from unittest.mock import patch, MagicMock, mock_open

from khmer_nlp_toolkits.commoncrawl import quality_warning as qw


FIXTURE_DIR = Path(__file__).parent / "fixtures/quality_warning"


@pytest.mark.parametrize("context_path, exp_qua_output", [
    (0, ['header']),
    (1, ['short_sentences', 'header', 'footer']),
    (2, ['short_sentences', 'footer']),
    (3, ['short_sentences', 'header', 'footer']),
    (4, ['short_sentences', 'header', 'footer']),
    (5, ['short_sentences', 'header', 'footer']),
    (6, ['footer']),
    (7, ['footer']),
    (8, ['header']),
    (9, ['short_sentences', 'header', 'footer']),
    (10, ['short_sentences', 'header', 'footer']),
    (11, ['noisy', 'short_sentences']),
    (12, ['tiny']),
    (13, ['noisy', 'tiny']),
    (14, ['footer']),
    (15, ['footer']),
    (16, ['footer']),
    (17, ['noisy', 'footer']),
    (18, None),
    (19, ['tiny']),
    (20, ['noisy', 'footer'])
])
def test_check_quality_warning(context_path, exp_qua_output):
    """
    clean data by check quality warning
    """
    with open(f"{FIXTURE_DIR}/context{context_path}.txt", "r") as reader:
        context = reader.read()
        output = qw.check_quality_warning(context)
        assert output == exp_qua_output


def test_check_quality_warning_type_error():
    with pytest.raises(TypeError, match="context must be a str."):
        qw.check_quality_warning(["abc"])

    with pytest.raises(ValueError, match="String is empty."):
        qw.check_quality_warning("")
