import pytest
from src.text import clean


"""
enclosing_symbol_consistency
"""


@pytest.mark.skip(reason="Function not implemented yet")
@pytest.mark.parametrize("input_str, output_str", [
    (["Pa(rent)hes)es"], "Pa(rent)heses"),
    (["Square[[] Brackets"], "Square[] Brackets"),
    (["{Curly} {Braces"], "{Curly} Braces"),
    (["<Angle <Brackets>"], "Angle <Brackets>"),
    (["[Mix {(enclosing})] symbol"], "[Mix {enclosing}] symbol")
])
def test_enclosing_symbol_consistency(input_str, output_str):
    assert clean.enclosing_symbol_consistency(*input_str) == output_str


"""
repetitive_punctuation
"""


@pytest.mark.skip(reason="Function not implemented yet")
@pytest.mark.parametrize("input_str, output_str", [
    (["Hello!!!"], "Hello!"),
    (["What???"], "What?"),
    (["Ehhh ..."], "Ehh ."),
    (["Mix!!! Punc,,,"], "Mix! Punc,")
])
def test_repetitive_punctuation(input_str, output_str):
    assert clean.repetitive_punctuation(*input_str) == output_str


"""
Space handler
"""


@pytest.mark.skip(reason="Function not implemented yet")
@pytest.mark.parametrize("input_str, output_str", [
    (["\u179f\u17bd\u200b\u179f\u17d2\u178a\u17b8"], "\u179f\u17bd\u179f\u17d2\u178a\u17b8"),
    (["\u179f\u17bd\u200b\u179f\u17d2\u178a\u17b8\u0020"], "\u179f\u17bd\u179f\u17d2\u178a\u17b8"),
    (["សួស្ដីhello"], "សួស្ដី hello"),
    (["សួ​ស្ដី helloសួស្ដី "], "សួ​ស្ដី hello សួស្ដី"),
    (["សួ​ស្ដី hello សួ​ស្ដី"], "សួ​ស្ដី hello សួ​ស្ដី"),
    (["Hello  how are you?"], "Hello how are you?"),
    (["Hello ​how are  you?"], "Hello how are you?"),
])
def test_space_handler(input_str, output_str):
    assert clean.space_handler(*input_str) == output_str


"""
Remove emoji.
"""


@pytest.mark.skip(reason="Function not implemented yet")
@pytest.mark.parametrize("input_str, output_str", [
    (["Hello, world! 🌍✨"], "Hello, world!"),
    (["Coding is fun! 💻🚀"], "Coding is fun!"),
    (["Movie night! 🎬🍿"], "Movie night!"),
    (["Let's go on an adventure! 🏕️🌲"], "Let's go on an adventure!"),
    (["Pizza night! 🍕"], "Pizza night!"),
    (["specific with emojis? 😃"], "specific with emojis?"),
    (["🎂🎈Happy Birthday! 🎂🎈"], "Happy Birthday!"),
])
def test_remvoe_emoji(input_str, output_str):
    assert clean.remove_emoji(*input_str) == output_str
