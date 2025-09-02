import pytest 
from khmer-nlp-toolkits.number.number import num2text


@pytest.mark.parametrize("exp_input, exp_output", [
    ([23], "ម្ភៃបី"),
    ([10_023], "មួយម៉ឺនម្ភៃបី"),
    ([6_200_054], "ប្រាំមួយលានពីរសែនហាសិបបួន"),
    ([6_200_054, "3"], "ប្រាំមួយលានពីររយពាន់ហាសិបបួន"),
])
def test_num2text(exp_input, exp_output):
    output = num2text(*exp_input)
    assert output == exp_output
