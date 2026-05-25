import pytest 
from khmer_nlp_toolkits.number.number import num2text


@pytest.mark.parametrize("exp_input", [
    "string",
    None,
    [1, 2],
    {"a": 1},
])
def test_num2text_reject_types_for_num(exp_input):
    with pytest.raises(TypeError):
        num2text(exp_input)


@pytest.mark.parametrize("exp_input, exp_output", [
    ([23], "ម្ភៃបី"),
    ([10_023], "មួយម៉ឺនម្ភៃបី"),
    ([6_200_054], "ប្រាំមួយលានពីរសែនហាសិបបួន"),
    ([1_102_006_200_054], "មួយទ្រីលានមួយរយពីរប៊ីលានប្រាំមួយលានពីរសែនហាសិបបួន"),
])
def test_num2text_int_normal(exp_input, exp_output):
    output = num2text(*exp_input)
    assert output == exp_output


@pytest.mark.parametrize("exp_input, exp_output", [
    ([23, "3"], "ម្ភៃបី"),
    ([10_023, "3"], "ដប់ពាន់ម្ភៃបី"),
    ([6_200_054, "3"], "ប្រាំមួយលានពីររយពាន់ហាសិបបួន"),
    ([1_102_006_200_054, "3"], "មួយទ្រីលានមួយរយពីរប៊ីលានប្រាំមួយលានពីររយពាន់ហាសិបបួន"),
])
def test_num2text_int_3(exp_input, exp_output):
    output = num2text(*exp_input)
    assert output == exp_output


@pytest.mark.parametrize("exp_input, exp_output", [
    ([0.123], "សូន្យចុចមួយរយម្ភៃបី"),
    ([23.0], "ម្ភៃបីចុចសូន្យ"),
    ([10.023], "ដប់ចុចសូន្យម្ភៃបី"),
    ([6.00054], "ប្រាំមួយចុចសូន្យសូន្យសូន្យហាសិបបួន"),
    ([600.054], "ប្រាំមួយរយចុចសូន្យហាសិបបួន"),
    ([6.200_054], "ប្រាំមួយចុចពីរសែនហាសិបបួន"),
])
def test_num2text_float_normal(exp_input, exp_output):
    output = num2text(*exp_input)
    assert output == exp_output


@pytest.mark.parametrize("exp_input, exp_output", [
    ([0.1123, "3"], "សូន្យចុចមួយពាន់មួយរយម្ភៃបី"),
    ([23.0, "3"], "ម្ភៃបីចុចសូន្យ"),
    ([10.023, "3"], "ដប់ចុចសូន្យម្ភៃបី"),
    ([6.00054, "3"], "ប្រាំមួយចុចសូន្យសូន្យសូន្យហាសិបបួន"),
    ([600.054, "3"], "ប្រាំមួយរយចុចសូន្យហាសិបបួន"),
    ([6.200_054, "3"], "ប្រាំមួយចុចពីររយពាន់ហាសិបបួន"),
    ([16001.200_054, "3"], "ដប់ប្រាំមួយពាន់មួយចុចពីររយពាន់ហាសិបបួន"),
])
def test_num2text_float_3(exp_input, exp_output):
    output = num2text(*exp_input)
    assert output == exp_output
