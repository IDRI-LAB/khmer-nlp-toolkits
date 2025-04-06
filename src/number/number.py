import math
from typing import Union, Literal

ONE_DIGIT = {
    "0": "សូន្យ",
    "1": "មួយ",
    "2": "ពីរ",
    "3": "បី",
    "4": "បួន",
    "5": "ប្រាំ",
    "6": "ប្រាំមួយ",
    "7": "ប្រាំពីរ",
    "8": "ប្រាំបី",
    "9": "ប្រាំបួន"
}
TWO_DIGITS = {
    "1":"ដប់",
    "2":"ម្ភៃ",
    "3":"សាមសិប",
    "4":"សែសិប",
    "5":"ហាសិប",
    "6":"ហុកសិប",
    "7":"ចិតសិប",
    "8":"ប៉ែតសិប",
    "9":"កៅសិប"
}
DIGIT_LEVEL = {
    3:"រយ",
    4:"ពាន់",
    5:"ម៉ឺន",
    6:"សែន",
    7:"លាន",
    10:"ប៊ីលាន",
    13:"ទ្រីលាន"
}


def num2text(num: Union[int, float], style: Literal["normal", "3"] = "normal", is_split: bool = False):
    """
    Generate number to text in various style for khmer lanugage.

    Parameters
    ==========
    num: Union[int, float]
        Number to convert to text.
    style: Literal["normal", "3"], default="normal"
        The style of reading number that will use to convert to text.
        "normal" mean read number one digit at a time with their value range.
        Ex: 100123 => "មួយសែនមួយរយម្ភៃបី"
        "3" mean read number 3 digit at a time (read in thousand).
        Ex: 100123 => "មួយរយពាន់មួយរយម្ភៃបី"
    is_split: bool, default=False
        If True, the return will be a list of text in each digit.
        Ex: 100123 => ["មួយសែន", "មួយរយ", "ម្ភៃ", "បី"]
    
    Return
    ======
    Union["str", "list[str]"]
    """
    # validated parameter
    if style not in ["normal", "3"]:
        raise ValueError(f"style must be one of ['normal', '3'] but given {style}")

    def generate_text_style(num_str, style: str):
        
        def split_num_str(num_str: list, style: int):
            # find num of bucket
            buc_threshold = sorted([10000, 12, 9, 6, 4, 0], reverse=True)
            group_num_str = []
            for maxv, minv in zip(buc_threshold[:-1], buc_threshold[1:]):
                group_num_str.append([num for num in num_str if minv <len(num) <= maxv])
            return group_num_str

        def generate(num_str, style):
            text = []
            if style in ("normal", "3"):
                grouped_num_str = split_num_str(num_str, 3)
                # print(grouped_num_str)
                for group in grouped_num_str:
                    if len(group) == 0:
                        continue
                    elif len(group[0]) >= 13:
                        text.append(generate_text_normal([str(int(int(num)/10**12)) for num in group]))
                        text.append([DIGIT_LEVEL[13]])
                    elif len(group[0]) >= 10:
                        text.append(generate_text_normal([str(int(int(num)/10**9)) for num in group]))
                        text.append([DIGIT_LEVEL[10]])
                    elif len(group[0]) >= 7:
                        text.append(generate_text_normal([str(int(int(num)/10**6)) for num in group]))
                        text.append([DIGIT_LEVEL[7]])
                    elif len(group[0]) >= 4 and style == "3":
                        text.append(generate_text_normal([str(int(int(num)/10**3)) for num in group]))
                        text.append([DIGIT_LEVEL[4]])
                    else:
                        text.append(generate_text_normal(group))
                return text
            # elif style == "3":
            #     grouped_num_str = split_num_str(num_str, 3)
            #     pass
        
        return generate(num_str, style)

    def generate_text_normal(num_str):
        text = []
        for ele in num_str:
            if ele == ".":
                text.append("ចុច")
            elif len(ele) == 1:
                text.append(ONE_DIGIT[ele[0]])
            elif len(ele) == 2:
                text.append(TWO_DIGITS[ele[0]])
            else:
                text.append(ONE_DIGIT[ele[0]] + DIGIT_LEVEL[len(ele)])
        return text


    def __divided_num(num: Union[int, float]):
        """
        Divide number into digit level.

        Parameters
        ----------
        num: Union[int|float]
            Number to split.
        
        Return
        ------
        list of str.
            Ex: 123 -> ["100", "20", "3"]
            Ex: 12.34 -> ["10", "2", ".", "30", "4"]
        """
        def divided_to_str(num: str):
            if num == "0":
                return ["0"]
            frac_zero = ["0"] * (len(num) - len(str(int(num))))
            return frac_zero + [num[i]+"0"*(len(num)-1-i) for i in range(len(num)) if num[i] != "0"]

        if isinstance(num, int):
            return divided_to_str(str(num))
            
        elif isinstance(num, float):
            int_part, frac_part = str(num).split(".")
            int_part = divided_to_str(int_part)
            frac_part = divided_to_str(frac_part)
            return int_part + ["."] + frac_part

        else:
            raise TypeError(f"Value must be int or float. Given {type(num)}")
    

    
    num_str = __divided_num(num)
    if "." not in num_str:
        gen_text = generate_text_style(num_str, style)
        gen_text = [text for i in gen_text for text in i]
        if is_split:
            return gen_text
        return "".join(gen_text)


if __name__ == "__main__":
    print(num2text(100123, "3", is_split=True))