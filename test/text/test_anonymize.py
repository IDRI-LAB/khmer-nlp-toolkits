import pytest
from khmer_nlp_toolkits.text import anonymize as ano



"""
Replace/Remove URL
"""
@pytest.mark.parametrize("input_str, output_str", [
    (["Visit my blog at http://myblog.com for updates."], "Visit my blog at [URL] for updates."),
    (["Secure link: https://secure.example.com/login"], "Secure link: [URL]"),
    (["Check out www.example.org/resources", "[url]"], "Check out [url]"),
    (["Links: http://one.com and https://two.org/docs", "[URL]"], "Links: [URL] and [URL]"),
    (["This sentence has no link.", "[URL]"], "This sentence has no link."),
    (["Google it: https://www.google.com/search?q=bert+model", "[URL]"], "Google it: [URL]"),
    (["Here's a weird one: go to www.example.com now!", "[URL]"], "Here's a weird one: go to [URL] now!"),
    (["Try youtube.com/watch?v=abc123", ""], "Try "),
    (["Send feedback to support.example.com or call us.", ""], "Send feedback to  or call us.")
])
def test_replace_url(input_str, output_str):
    assert ano.replace_url(*input_str) == output_str


@pytest.mark.parametrize("input_str, output_str", 
[
    # Basic formats
    (["TEL:0234567890"], "TEL:[TEL]"),
    (["Phone: 023-456-7890"], "Phone: [TEL]"),
    (["Office: (023) 456-789", "[tel]"], "Office: [tel]"),
    (["Mobile: +1 123 456 7890", "[tel]"], "Mobile: [tel]"),
    (["Emergency: +1 (123) 456-7890", "[phone]"], "Emergency: [phone]"),
    # International
    (["UK: +44 20 7946 0958", "[TEL]"], "UK: [TEL]"),
    (["JP: +81-90-1234-5678", "[TEL]"], "JP: [TEL]"),
    (["KH: +855 12 345 678", "[TEL]"], "KH: [TEL]"),
    (["FR: +33 1 42 68 53 00", "[TEL]"], "FR: [TEL]"),
    # Extensions
    (["Dial 023-456-7890 ext 55", "[TEL]"], "Dial [TEL] ext 55"),
    (["Support: (023)456-7890 x1234", "[TEL]"], "Support: [TEL] x1234"),
    # Multiple numbers
    (["Home: 011-222-3333, Work: 044-555-6666", "[TEL]"], "Home: [TEL], Work: [TEL]"),
    (["Call +1 123 456 7890 or +855 98 765 432", "[TEL]"], "Call [TEL] or [TEL]"),
    # Invalid / should probably NOT match
    (["Order ID: 123456", "[TEL]"], "Order ID: 123456"),
    (["Version 1.2.3.4567", "[TEL]"], "Version 1.2.3.4567"),
    (["Random digits 111222", "[TEL]"], "Random digits 111222"),
    (["IP address 192.168.1.1", "[TEL]"], "IP address 192.168.1.1"),
    # Extremely formatted
    (["+1-(123)-456--7890", "[TEL]"], "[TEL]"),
    (["+855(0)12345678", "[TEL]"], "[TEL]"),
    # Embedded text
    (["abc1234567890xyz", "[TEL]"], "abc1234567890xyz"),
    (["tel:+1-123-456-7890", "[TEL]"], "tel:[TEL]"),
    # Empty / boundary
    (["", "[TEL]"], ""),
    (["No phone number here", "[TEL]"], "No phone number here"),
])
def test_replace_tel(input_str, output_str):
    assert ano.replace_tel(*input_str) == output_str



@pytest.mark.parametrize("input_str, output_str", [
    # Multiple emails
    (
        ["Send to alice@example.com and bob@test.org"],
        "Send to [EML] and [EML]",
    ),
    # Subdomains
    (
        ["admin@mail.service.company.co.uk", ""],
        "",
    ),

    # Plus alias
    (
        ["john+dev@gmail.com", "[EMAIL]"],
        "[EMAIL]",
    ),

    # Uppercase
    (
        ["TEST.USER@EXAMPLE.COM", "[EMAIL]"],
        "[EMAIL]",
    ),

    # Mixed content
    (
        ["Website example.com email help@example.com", "[EMAIL]"],
        "Website example.com email [EMAIL]",
    ),

    # Surrounded by punctuation
    (
        ["<test@example.com>", "[EMAIL]"],
        "<[EMAIL]>",
    ),
    (
        ['"user@test.org"', "[EMAIL]"],
        '"[EMAIL]"',
    ),

    # Invalid emails
    (
        ["abc@@example.com", "[EMAIL]"],
        "abc@@example.com",
    ),
    (
        ["missing-domain@test", "[EMAIL]"],
        "missing-domain@test",
    ),
    (
        ["@example.com", "[EMAIL]"],
        "@example.com",
    ),
    # Newlines
    (
        ["Email:\ntest@example.com", "[EMAIL]"],
        "Email:\n[EMAIL]",
    ),
    # Empty / boundary
    (
        ["", "[EMAIL]"],
        "",
    ),
    (
        ["No email here", "[EMAIL]"],
        "No email here",
    ),
])
def test_replace_email(input_str, output_str):
    assert ano.replace_email(*input_str) == output_str



@pytest.mark.parametrize("input_str, output_str", [
    # Mixed TEL + EMAIL + URL
    (
        (
            "Contact john@example.com or call 012-345-678. "
            "Website: https://example.com"
        ),
        (
            "Contact [EML] or call [TEL]. "
            "Website: [URL]"
        ),
    ),
    (
        (
            "Website: https://example.com "
            "Contact john@example.com or call 012-345-678."
        ),
        (
            "Website: [URL] "
            "Contact [EML] or call [TEL]."
        ),
    ),
    # Multiple entity types
    (
        (
            "Email admin@test.org, backup: help@company.com, "
            "TEL 098-765-432"
        ),
        (
            "Email [EML], backup: [EML], "
            "TEL [TEL]"
        )
    ),
    # URL containing digits should not become TEL
    (
        (
            "Visit https://example.com/2024/report "
            "or call 023-456-7890"
        ),
        (
            "Visit [URL] "
            "or call [TEL]"
        )
    ),
    # Email domain should not become URL separately
    (
        "Send mail to dev.team@example.com",
        "Send mail to [EML]"
    ),
    # TEL inside URL query
    (
        "https://example.com/?phone=012345678",
        "[URL]"
    ),
    # Multiple URLs
    (
        "Docs: https://a.com and https://b.org",
        "Docs: [URL] and [URL]"
    ),
    # Adjacent punctuation
    (
        "Email: <user@example.com>, TEL: (023)-456-7890!",
        "Email: <[EML]>, TEL: [TEL]!"
    ),
    # No PII
    ("", ""),
    (
        "This text contains no personal info.",
        "This text contains no personal info."
    ),
])
def test_anonymizer(input_str, output_str):
    assert ano.anonymizer(input_str) == output_str