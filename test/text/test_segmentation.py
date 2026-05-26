import pytest
from pytest_mock import mocker

from khmer_nlp_toolkits.text import segmentation as seg


"""
Sentence segmentation.
"""
@pytest.mark.parametrize("test_filepath", [5, 9, 11, 15, 18, 21])
def test_remove_repetitive_punc(test_filepath):
    with open(f"test/text/fixture/segmentation/context{test_filepath}.txt", 'r') as reader:
        input_str, output_str = reader.read().split("\n====================\n")
    assert seg.sentence_segment(input_str) == output_str.split("\n")


"""
Paragraph segmentation.
"""
@pytest.mark.parametrize("test_filepath, exp_output", [
    [5, 2],
    [9, 2],
    [11, 1],
    [15, 1],
    [18, 1],
    [21, 3],
])
def test_remove_repetitive_punc(test_filepath, exp_output):
    with open(f"test/text/fixture/segmentation/context{test_filepath}.txt", 'r') as reader:
        input_str, _ = reader.read().split("\n====================\n")
    assert len(seg.paragraph_segment(input_str)) == exp_output


def test_input_word_segmentation():
    with pytest.raises(ValueError, match="The word type must be 'com' or 'mor'."):
        seg.word_segment("Hello", "abc")
        seg.word_segment("Hello", "COM")
        seg.word_segment("Hello", 1)


def test_word_segment_call_correct_func(mocker):
    mock1 = mocker.patch("khmer_nlp_toolkits.text.segmentation._load_tokenizer")
    mock2 = mocker.patch("khmer_nlp_toolkits.text.segmentation.word_tokenize")

    seg.word_segment("Hello", "mor")
    mock1.assert_called_once()
    mock2.assert_not_called()

    mock1.reset_mock()
    mock2.reset_mock()

    seg.word_segment("Hello", "com")
    mock1.assert_not_called()
    mock2.assert_called_once()


def test_kcc_seg(mocker):
    mock = mocker.patch("khmer_nlp_toolkits.text.segmentation.seg_kcc")

    seg.kcc_segment("hello")
    mock.assert_called_once()
