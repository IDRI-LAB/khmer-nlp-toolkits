"""
This module is for cleaning specific spider. This function should be use before text clean.
"""
import re


AKP = re.compile(r"[(akp)|(kp)]?.{0,20}ថ្ងៃ.{0,30}?\d{3,4}[\u200b\ \n\-\+\–\—\_]{0,5}", re.IGNORECASE|re.DOTALL)


def scrape_cleaner(obj):
    obj["metadata"]["more"] = []
    # special target website
    if obj["metadata"]["spider_name"] == "ipdefenseforum":
        obj["content"] = obj["content"].replace("ទស្សនាវដ្តី FORUM បានផ្អាកការបកប្រែអត្ថបទប្រចាំថ្ងៃសម្រាប់គេហទំព័រជាភាសាខ្មែរ។ សូមមើលភាសាដទៃទៀតសម្រាប់ខ្លឹមសារប្រចាំថ្ងៃ។", "")  # noqa: E501
        texts = obj["content"].split("\n", maxsplit=1)
        if len(texts[0]) < 100:
            obj["metadata"]["more"].append(texts[0])
            obj["content"] = texts[1].strip()

        texts = obj["content"].rsplit("\n", maxsplit=1)
        if "រូបភាព៖" in texts[1]:
            obj["metadata"]["more"].append(texts[1])
            obj["content"] = texts[0]
    elif obj["metadata"]["spider_name"] == "bizkhmer":
        obj["content"] = re.sub(r"\[caption.*?caption\]", "", obj["content"], flags=re.DOTALL)
    elif obj["metadata"]["spider_name"] == "akp":
        texts = AKP.split(obj["content"], maxsplit=1)
        if len(texts) > 1 and len(texts[0]) < 50:
            obj["metadata"]["more"].append(texts[0])
            obj["content"] = texts[1]
    elif obj["metadata"]["spider_name"] == "khmerload":
        obj["content"] = obj["content"].split("ដោយឡែកព័ត៌មានគួរឲ្យចាប់អារម្មណ៍មួយផ្សេងទៀត៖")[0]
    elif obj["metadata"]["spider_name"] == "khmerplace":
        obj["content"] = obj["content"].split("ពត៌មានទំនាក់ទំនង៖")[0]
    elif obj["metadata"]["spider_name"] == "camnews_org":
        content = []
        texts = texts = re.sub(r"\n\|\n?", "|", obj["content"]).split("\n")
        for te in texts[:6]:
            if len(te) <= 25 or "|" in te:
                obj["metadata"]["more"].append(te)
            else:
                content.append(te)
        content += texts[6:]
        obj["content"] = "\n".join(content)

    # check beginning of content
    texts = re.split(r'[\៖\:]', obj["content"], maxsplit=1)
    if len(texts[0]) < 50:
        obj["metadata"]["more"].append(texts[0])
        obj["content"] = texts[1]
    # check end of paragraph
    texts = obj["content"].rsplit("៕", maxsplit=1)
    if len(texts) == 1 or texts[1] == "":
        return obj
    obj["metadata"]["more"].append(texts[1])
    obj["content"] = texts[0]+"៕"
    return obj
