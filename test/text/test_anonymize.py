import pytest
from khmer_nlp_toolkits.text import anonymize



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
    assert anonymize.replace_url(*input_str) == output_str
