import pytest

from khmer_nlp_toolkits.text import mask_lang as ml


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # English should remain
        (
            "hello world",
            "hello world",
        ),
        # Khmer should remain
        (
            "សួស្តី ពិភពលោក",
            "សួស្តី ពិភពលោក",
        ),
        # Greek should remain
        (
            "αβγδε",
            "αβγδε",
        ),
        # Chinese should be masked
        (
            "你好世界",
            "[UNK]",
        ),
        # Mixed language
        (
            "hello 你好 សួស្តី",
            "hello [UNK] សួស្តី",
        ),
        # Emoji/symbols should remain because of \p{S}
        (
            "hello 😊",
            "hello 😊",
        ),
        # Japanese should be masked
        (
            "こんにちは",
            "[UNK]",
        ),
        # Multiple unknown blocks collapse into one mask
        (
            "hello 中文 日本語",
            "hello [UNK] [UNK]",
        ),
    ],
)
def test_lang_masking(text, expected):
    assert ml.lang_masking(text) == expected
