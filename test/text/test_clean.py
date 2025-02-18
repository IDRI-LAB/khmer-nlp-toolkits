import pytest
from src.text import clean


"""
enclosing_symbol_consistency
"""
@pytest.mark.skip(reason="Function not implemented yet")
@pytest.mark.parametrize("input_str, output_str", [
    (("\"Double\"\" Quotes"), "\"Double\" Quotes"),
    (("\'\'Single\' Quotes"), "\'Double\' Quotes"),
    (("Pa(rent)hes)es"), "Pa(rent)heses"),
    (("Square[[] Brackets"), "Square[] Brackets"),
    (("{Curly} {Braces"), "{Curly} Braces"),
    (("<Angle <Brackets>"), "Angle <Brackets>"),
    (("[Mix {(enclosing})] symbol"), "[Mix {enclosing}] symbol")
])
def test_enclosing_symbol_consistency(input_str, output_str):
    assert clean.enclosing_symbol_consistency(*input_str) == output_str


"""
repetitive_punctuation
"""
@pytest.mark.skip(reason="Function not implemented yet")
@pytest.mark.parametrize("input_str, output_str", [
    (("Hello!!!"), "Hello!"),
    (("What???"), "What?"),
    (("Ehhh ..."), "Ehh ."),
    (("Mix!!! Punc,,,"), "Mix! Punc,")
])
def test_repetitive_punctuation(input_str, output_str):
    assert clean.repetitive_punctuation(*input_str) == output_str

