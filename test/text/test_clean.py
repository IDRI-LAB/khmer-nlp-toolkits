import pytest
from src.text import clean


"""
repetitive_punctuation
"""
@pytest.mark.parametrize("input_str, output_str", [
    (["Hello!!!"], "Hello!"),
    (["What???"], "What?"),
    (["Ehhh ..."], "Ehhh ."),
    (["Mix!!! Punc,,,"], "Mix! Punc,"),
    (["Mix!!???"], "Mix!?")
])
def test_remove_repetitive_punc(input_str, output_str):
    assert clean.remove_repetitive_punc(*input_str) == output_str


"""
Space handler
- Remove hidden space
- Trimming include \u200b
- Add single space around english word boundary if not exist
- Remove repetitive whitespace
"""
@pytest.mark.parametrize("input_str, output_str", [
    (["\u179f\u17bd\u200b\u179f\u17d2\u178a\u17b8"], "\u179f\u17bd\u179f\u17d2\u178a\u17b8"),
    (["\u179f\u17bd\u200b\u179f\u17d2\u178a\u17b8\u0020"], "\u179f\u17bd\u179f\u17d2\u178a\u17b8"),
    (["សួស្ដីhello"], "សួស្ដី hello"),
    (["សួ​ស្ដី helloសួស្ដី "], "សួស្ដី hello សួស្ដី"),
    (["សួ​ស្ដី hello សួ​ស្ដី"], "សួស្ដី hello សួស្ដី"),
    (["Hello  how are you?"], "Hello how are you?"),
    (["Hello ​how are  you?"], "Hello how are you?"),
    (["\u200bHello how are  you? \u200b"], "Hello how are you?"),
])
def test_space_handler(input_str, output_str):
    assert clean.space_handler(*input_str) == output_str


"""
Remove emoji.
"""
@pytest.mark.parametrize("input_str, output_str", [
    (["Hello, world! 🌍✨"], "Hello, world!"),
    (["Coding is fun! 💻🚀"], "Coding is fun!"),
    (["Movie night! 🎬🍿"], "Movie night!"),
    (["Let's go on an adventure! 🏕️🌲"], "Let's go on an adventure!"),
    (["Pizza night! 🍕"], "Pizza night!"),
    (["specific with emojis? 😃"], "specific with emojis?"),
    (["🎂🎈Happy Birthday! 🎂🎈"], "Happy Birthday!"),
])
def test_remove_misc_symbols(input_str, output_str):
    assert clean.remove_misc_symbols(*input_str) == output_str


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
Replace/Remove URL
"""
@pytest.mark.parametrize("input_str, output_str", [
    (["Visit my blog at http://myblog.com for updates.", "[URL]"], "Visit my blog at [URL] for updates."),
    (["Secure link: https://secure.example.com/login", "[URL]"], "Secure link: [URL]"),
    (["Check out www.example.org/resources", "[URL]"], "Check out [URL]"),
    (["Links: http://one.com and https://two.org/docs", "[URL]"], "Links: [URL] and [URL]"),
    (["This sentence has no link.", "[URL]"], "This sentence has no link."),
    (["Google it: https://www.google.com/search?q=bert+model", "[URL]"], "Google it: [URL]"),
    (["Here's a weird one: go to www.example.com now!", "[URL]"], "Here's a weird one: go to [URL] now!"),
    (["Try youtube.com/watch?v=abc123"], "Try "),
    (["Send feedback to support.example.com or call us."], "Send feedback to  or call us.")
])
def test_replace_url(input_str, output_str):
    assert clean.replace_url(*input_str) == output_str

