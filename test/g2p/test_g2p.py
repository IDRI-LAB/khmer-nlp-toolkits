import pytest

from khmer_nlp_toolkits.g2p import engine
from khmer_nlp_toolkits.g2p import g2p, g2p_word, g2p_words, TARGETS


try:
    import sosap  # noqa: F401 pylint: disable=W0611
    HAS_SOSAP = True
except ImportError:
    HAS_SOSAP = False

requires_sosap = pytest.mark.skipif(not HAS_SOSAP, reason="sosap needs Python 3.11+.")


@pytest.fixture(autouse=True)
def clear_cache():
    engine._CACHE.clear()
    yield
    engine._CACHE.clear()


@pytest.fixture
def fake_predict(mocker):
    """Replace the model call with a deterministic fake: every letter becomes one phoneme."""
    return mocker.patch.object(engine, "_predict", side_effect=lambda words, target: {w: list(w) for w in words})


"""
Input validation.
"""
def test_invalid_target():
    with pytest.raises(ValueError):
        g2p_word("ខ្មែរ", target="arpabet")
    with pytest.raises(ValueError):
        g2p("ខ្មែរ", target="arpabet")


def test_invalid_types():
    with pytest.raises(TypeError):
        g2p_word(["ខ្មែរ"])
    with pytest.raises(TypeError):
        g2p_words("ខ្មែរ")
    with pytest.raises(TypeError):
        g2p(123)


def test_invalid_rt_type():
    with pytest.raises(ValueError):
        g2p("ខ្មែរ", rt_type="dict")


"""
Logic with a mocked model.
"""
def test_words_batched_and_cached(fake_predict):
    assert g2p_words(["កា", "កា", "ខ"]) == [["ក", "ា"], ["ក", "ា"], ["ខ"]]
    assert fake_predict.call_count == 1
    assert sorted(fake_predict.call_args[0][0]) == ["កា", "ខ"]

    g2p_words(["កា", "ខ"])
    assert fake_predict.call_count == 1  # served from cache


def test_non_khmer_words_skip_model(fake_predict):
    assert g2p_words(["hello", "123", "។", "១២"]) == [[], [], [], []]
    fake_predict.assert_not_called()


def test_cache_is_per_target(fake_predict):
    g2p_word("កា", "ipa")
    g2p_word("កា", "tts")
    assert fake_predict.call_count == 2


def test_cache_limit(fake_predict, mocker):
    mocker.patch.object(engine, "_CACHE_LIMIT", 2)
    g2p_words(["ក", "ខ"])
    g2p_words(["គ"])
    assert len(engine._CACHE) == 1


def test_text_keeps_non_khmer_tokens(fake_predict):
    assert g2p("ក hello ។") == "ក | hello | ។"
    assert g2p("ក hello ។", word_sep="_") == "ក_hello_។"


def test_text_list_output(fake_predict):
    assert g2p("ក hello", rt_type="list") == [("ក", ["ក"]), ("hello", ["hello"])]


def test_numbers_not_expanded_by_default(fake_predict):
    assert g2p("១២", rt_type="list") == [("១២", ["១២"])]
    fake_predict.assert_not_called()


def test_text_expand_numbers(fake_predict):
    tokens = [tok for tok, _ in g2p("១២", rt_type="list", expand_numbers=True)]
    assert tokens == ["ដប់", "ពីរ"]


def test_khmer_word_kept_next_to_numbers(fake_predict):
    assert [tok for tok, _ in g2p("ក ១០", rt_type="list", expand_numbers=True)] == ["ក", "ដប់"]


def test_missing_sosap(mocker):
    engine._load_model.cache_clear()
    mocker.patch.dict("sys.modules", {"sosap": None})
    with pytest.raises(RuntimeError, match="sosap"):
        engine._load_model("ipa")
    engine._load_model.cache_clear()


def test_missing_model_output_gives_empty(mocker):
    mocker.patch.object(engine, "_predict", return_value={})
    assert g2p_word("កា") == []


def test_missing_model_file(mocker, tmp_path):
    mocker.patch.object(engine, "MODEL_DIR", tmp_path)
    with pytest.raises(FileNotFoundError):
        engine._model_path("ipa")


def test_predict_drops_empty_phonemes(mocker):
    fake_model = mocker.Mock()
    fake_model.phoneticize.return_value = ["a", "", "b"]
    mocker.patch.object(engine, "_load_model", return_value=fake_model)
    assert engine._predict(["ក"], "ipa") == {"ក": ["a", "b"]}


@requires_sosap
def test_model_loaded_once_per_target():
    engine._load_model.cache_clear()
    assert engine._load_model("ipa") is engine._load_model("ipa")
    assert engine._load_model("ipa") is not engine._load_model("tts")


"""
End-to-end with the packaged models.
"""
@requires_sosap
@pytest.mark.parametrize("target, expected", [
    ("ipa", ["kʰ", "m", "aɛ"]),
    ("latin", ["kh", "m", "ae"]),
    ("tts", ["KH", "M", "ea:"]),
])
def test_word_all_targets(target, expected):
    assert g2p_word("ខ្មែរ", target) == expected


@requires_sosap
def test_text_end_to_end():
    assert g2p("ភាសាខ្មែរ", target="ipa") == "pʰ iɜ s aː | kʰ m aɛ"
    assert g2p("ភាសាខ្មែរ", target="ipa", word_sep=" ") == "pʰ iɜ s aː kʰ m aɛ"


def test_targets_constant():
    assert TARGETS == ("ipa", "latin", "tts")


@requires_sosap
def test_no_empty_phonemes_in_tts_output():
    # Without filtering, the TTS model emits '' as a trailing phoneme for words like this.
    assert "" not in g2p_word("បង្គួរ", "tts")
    assert g2p_word("បង្គួរ", "tts") == ["B", "a", "NG", "K", "uor"]


@requires_sosap
def test_unknown_khmer_symbol_does_not_crash():
    assert isinstance(g2p_word("ៜ"), list)
