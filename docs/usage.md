# Usage Guidelines

This document contains detailed usage examples for Khmer NLP Toolkits.

---

# Table of Contents
- [Text Processing](#text-processing)
  - [Anonymize](#anonymize)
  - [Normalize](#normalize)
  - [Clean](#clean)
  - [Segmentation](#segmentation)

- [Number Processing](#number-processing)

- [Commoncrawl Processing](#commoncrawl-processing)

- [Deduplication](#deduplication)

- [Utilities](#utility-functions)

---

# Text Processing

## Anonymize

Replace entity or sensitive information such as phone numbers, emails, URLs or other PII with placeholder tokens.

### Available Functions

| Function | Description |
|---|---|
| `anonymizer` | Completed anonymize pipeline to replace sensitive information with placeholder tokens. |
| `replace_email` | Replace email addresses in text. |
| `replace_tel` | Replace telephone numbers in text. |
| `replace_url` | Replace URLs in text. |

### Function Details

<details>
<summary><strong><code>anonymizer()</code></strong></summary>

Replace entity and sensitive information with its placeholder token. Currently support only Phone numbers, Emails, URLs.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Anonymized text. |


<strong>Example</strong>
```python
from khmer_nlp_toolkits.text.anonymize import anonymizer

print(anonymizer("You can contact us by phone at +855 12 345 678, email us at support@example.com, or visit our website at https://www.example.com anytime."))
# You can contact us by phone at [TEL], email us at [EML], or visit our website at [URL] anytime.
```
---
</details>


<details>
<summary><strong><code>replace_url()</code></strong></summary>

Replace all url addresses in text with placeholder token.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |
| `replace` | `str` | Replace placeholder. |

| Type | Description |
|---|---|
| `str` | Anonymized text. |


<strong>Example</strong>:
```python
from khmer_nlp_toolkits.text.anonymize import replace_url

print(replace_url("visit our website at https://www.example.com, or our telegram channel t.me/example anytime."))
# visit our website at [URL] or our telegram channel [URL] anytime.
```
---
</details>

<details>
<summary><strong><code>replace_email()</code></strong></summary>

Replace all email addresses in text with placeholder token.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |
| `replace` | `str` | Replace placeholder. |

| Type | Description |
|---|---|
| `str` | Anonymized text. |


<strong>Example</strong>:
```python
from khmer_nlp_toolkits.text.anonymize import replace_email

print(replace_email("Send the doc to alice@example.com and bob@test.org by tmr."))
# Send the doc to [EML] and [EML] by tmr.
```
---
</details>

<details>
<summary><strong><code>replace_tel()</code></strong></summary>

Replace all telephone number in text with placeholder token.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |
| `replace` | `str` | Replace placeholder. |

| Type | Description |
|---|---|
| `str` | Anonymized text. |


<strong>Example</strong>:
```python
from khmer_nlp_toolkits.text.anonymize import replace_tel

print(replace_tel("Home: 011-222-3333, Work: 044-555-6666.", "[tel]"))
# Home: [tel], Work: [tel].
```
---
</details>

## Normalize

Utilities for Khmer text normalization.

### Available Functions

| Function | Description |
|---|---|
| `khnormal` | NormKhmer unicode disorder normalization function. |
| `normalizer` | Normalize text using Unicode NFKD, lowercase conversion, and Khmer normalization. |

### Function Detials

<details>
<summary><strong><code>khnormal()</code></strong></summary>

Khmer unicode encoding disorder normalization function. we use normalization script provided by [Hosken et al](#ref-2).

 Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Normaized text. |


<strong>Example</strong>:
```python
from khmer_nlp_toolkits.text.normalize import khnormal

text1 = "ធ្វើ"  # \u1792\u17d2\u179c\u17be
text2 = "ធ្វេី"  # \u1792\u17d2\u179c\u17c1\u17b8
text3 = khnormal(text2)

print(text1 == text2)
# False
print(text3 == text1)
# True
print(text3 == text2)
# False
```
---
</details>


<details>
<summary><strong><code>Normalizer()</code></strong></summary>

Normalizer function for both English and Khmer text. It normalize English character with
NFKD and lowercase follow by `khnormal()` for Khmer text.

**Noted:** NFDK are normalize in decomposition. It covert format character to the base character (ex: ＴＥＸＴ -> TEXT) and break composition character into base character and accents character (ex: à -> a + \u0300, é -> e + \u0301). This accents character will be remove in clean function.

Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Normaized text. |


<strong>Example</strong>:
```python
from khmer_nlp_toolkits.text.normalize import nomalizer


text = "Ｔhis is à tést ＴＥＸＴ for normalizer. ពាក្យធ្វេីនិងពាក្យស្រ្តីជាឧទាហរណ៍កុ្នងភាសាខែ្មរ។"
output = nomalizer(text)

print(output)
# this is à tést text for normalizer. ពាក្យធ្វើនិងពាក្យស្ត្រីជាឧទាហរណ៍ក្នុងភាសាខ្មែរ។
# OLD TEXT: \uff34\u0068\u0069\u0073\u0020\u0069\u0073\u0020\u00e0\u0020\u0074\u00e9\u0073\u0074\u0020\uff34\uff25\uff38\uff34\u0020\u0066\u006f\u0072\u0020\u006e\u006f\u0072\u006d\u0061\u006c\u0069\u007a\u0065\u0072\u002e\u0020\u1796\u17b6\u1780\u17d2\u1799\u1792\u17d2\u179c\u17c1\u17b8\u1793\u17b7\u1784\u1796\u17b6\u1780\u17d2\u1799\u179f\u17d2\u179a\u17d2\u178f\u17b8\u1787\u17b6\u17a7\u1791\u17b6\u17a0\u179a\u178e\u17cd\u1780\u17bb\u17d2\u1793\u1784\u1797\u17b6\u179f\u17b6\u1781\u17c2\u17d2\u1798\u179a\u17d4
# NEW TEXT: \u0074\u0068\u0069\u0073\u0020\u0069\u0073\u0020\u0061\u0300\u0020\u0074\u0065\u0301\u0073\u0074\u0020\u0074\u0065\u0078\u0074\u0020\u0066\u006f\u0072\u0020\u006e\u006f\u0072\u006d\u0061\u006c\u0069\u007a\u0065\u0072\u002e\u0020\u1796\u17b6\u1780\u17d2\u1799\u1792\u17d2\u179c\u17be\u1793\u17b7\u1784\u1796\u17b6\u1780\u17d2\u1799\u179f\u17d2\u178f\u17d2\u179a\u17b8\u1787\u17b6\u17a7\u1791\u17b6\u17a0\u179a\u178e\u17cd\u1780\u17d2\u1793\u17bb\u1784\u1797\u17b6\u179f\u17b6\u1781\u17d2\u1798\u17c2\u179a\u17d4
```
---
</details>

## Clean

Utilities  for text cleaning.

### Available Functions

| Function | Description |
|---|---|
| `text_cleaner` | Full option funciton for clean noisy text. |
| `remove_invisible_chars` | Remove invisible unicode characters. |
| `remove_misc_symbols` | This function will remove any miscellaneous symbols (monochrome emoji and colorful emoji). |
| `remove_repetitive_punc` | Remove/Normalize repeated punctuation symbols. |
| `space_handler` | Handle space cleaning and manipulation for khmer text. |
| `count_khmer_char` | Normalize dash symbols into standard format. |

### Function Details

<details>
<summary><strong><code>text_cleaner()</code></strong></summary>

Clean noisy text by cleaning invisible characters, duplicated spaces, repeated punctuation, formatting artifacts and more. The objective was to get the clean and structured corpus format.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Cleaned text. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.clean import text_cleaner

print(text_cleaner(
    "\u200b&nbsp;Hello\u2014\u2014World!!!??      ខ្មែរ   123\u200b&nbsp;"
))
# Hello - World !? ខ្មែរ 123
```
---
</details>


<details>
<summary><strong><code>remove_invisible_chars()</code></strong></summary>

Remove invisible unicode characters such as zero-width spaces and formatting artifacts. This unicode range was inspired by [Kaing et al.](#ref-1).



| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Cleaned text without invisible characters. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.clean import remove_invisible_chars

print(remove_invisible_chars("He\u2060llo\u200bWorld"))
# HelloWorld
```
---
</details>


<details>
<summary><strong><code>remove_misc_symbols()</code></strong></summary>

This function will remove any miscellaneous symbols (monochrome emoji and colorful emoji)
that are classify by unicodedata (So & Sk). Unicodedata categorize symbol character into 4 types
such as Math (Sm), Currency (Sc), Modifier (Sk), other (So).

**Noted:** In khmer character unicdoe range 1780-17FF (Khmer), There are no 'Sk'. And 19E0-19FF (Khmer Symbol) are 'So'.
Character type: https://www.fileformat.info/info/unicode/category/index.htm

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Text without miscellaneouse characters or symbols. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.clean import remove_misc_symbols

print(remove_misc_symbols("🎂🎈Happy Birthday! 🎂🎈"))
# Happy Birthday!
```
---
</details>


<details>
<summary><strong><code>remove_repetitive_punc()</code></strong></summary>

Remove/Normalize repeated punctuation symbols into cleaner formatting by keeping only one of its kind.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Text with normalized punctuation. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.clean import remove_repetitive_punc

print(remove_repetitive_punc("Hello!!!????"))
# Hello!?
```
---
</details>


<details>
<summary><strong><code>space_handler()</code></strong></summary>

Handle space cleaning and manipulation for khmer text.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `str` | Text with formated space. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.clean import space_handler

print(space_handler("សួ​ស្ដីis hello.(សួស្ដីalso mean Hi)"))
# សួស្ដី is hello . ( សួស្ដី also mean Hi )
```
---
</details>

## Segmentation

Utilities for Khmer text segmentation.

### Available Functions

| Function | Description |
|---|---|
| `sentence_segment` | Segment text into sentences. |
| `word_segment` | Segment Khmer text into words. |
| `kcc_segment` | Segment Khmer text into khmer character clustering (kcc). |

### Function Details

<details>
<summary><strong><code>sentence_segment()</code></strong></summary>

Segment text into sentence-level units.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `list[str]` | List of segmented sentences. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.segmentation import sentence_segment

text = "ខ្ញុំស្រឡាញ់ភាសាខ្មែរ។ នេះគឺជាការសាកល្បង។"

print(sentence_segment(text))
# ["ខ្ញុំស្រឡាញ់ភាសាខ្មែរ។", "នេះគឺជាការសាកល្បង។"]
```
---
</details>

<details>
<summary><strong><code>word_segment()</code></strong></summary>

Segment Khmer text into word-level tokens. Two type of segment available 'com' for compound level segmenation and 'mor' for morpheme level segmentation.

**Note:** It called [*Khmer-NLTK*](#ref-3) API for Compound segmenation, while using model from [*Khmer-NLP-Tools*](#ref-4) for Morpheme segmentation.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |
| `word_type` | `enum['com', 'mor']` | Segmentation type. Default = "com"|
| `rt_type` | `enum['str', 'list']` | Output type. Default = "str"|

| Type | Description |
|---|---|
| `str \| list[str]` | Result of segmented words. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.segmentation import word_segment

text = "នៅយប់ថ្ងៃទី៣១ ខែមីនា ឆ្នាំ២០២១នេះ វ៉ាក់សាំងកូវីដ១៩ ស៊ីណូហ្វាម ចំនួន ៧០ម៉ឺនដូស ជាជំនួយដ៏ ស្មោះសរបស់រដ្ឋាភិបាលចិន បានមកដល់កម្ពុជាហើយ។"


print(word_segment(text, word_type="com"))
# នៅ យប់ ថ្ងៃទី ៣១ ខែមីនា ឆ្នាំ ២០២១ នេះ វ៉ាក់សាំង កូវីដ១៩ ស៊ីណូ ហ្វាម ចំនួន ៧០ ម៉ឺន ដូស ជា ជំនួយ ដ៏ ស្មោះស របស់ រដ្ឋាភិបាល ចិន បាន មកដល់ កម្ពុជា ហើយ ។
print(word_segment(text, word_type="mor"))
# នៅ យប់ ថ្ងៃ ទី ៣១ ខែ មីនា ឆ្នាំ ២០២១ នេះ វ៉ាក់សាំង កូវីដ ១៩ ស៊ីណូ ហ្វាម ចំនួន ៧០ ម៉ឺន ដូស ជា ជំនួយ ដ៏ ស្មោះ ស របស់ រដ្ឋាភិបាល ចិន បាន មក ដល់ កម្ពុជា ហើយ ។
print(word_segment(text, rt_type='list'))
# ['នៅ', 'យប់', 'ថ្ងៃទី', '៣១', 'ខែមីនា', 'ឆ្នាំ', '២០២១', 'នេះ', 'វ៉ាក់សាំង', 'កូវីដ១៩', 'ស៊ីណូ', 'ហ្វាម', 'ចំនួន', '៧០', 'ម៉ឺន', 'ដូស', 'ជា', 'ជំនួយ', 'ដ៏', 'ស្មោះស', 'របស់', 'រដ្ឋាភិបាល', 'ចិន', 'បាន', 'មកដល់', 'កម្ពុជា', 'ហើយ', '។']

```
---
</details>

<details>
<summary><strong><code>kcc_segment()</code></strong></summary>

Segment text into kcc-level units.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text. |

| Type | Description |
|---|---|
| `list[str]` | List of kcc token. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.text.segmentation import kcc_segment

text = "ខ្ញុំស្រឡាញ់ភាសាខ្មែរ។"

print(kcc_segment(text))
# ['ខ្ញុំ', 'ស្រ', 'ឡា', 'ញ់', 'ភា', 'សា', 'ខ្មែ', 'រ', '។']
```
---
</details>

<br>

# Number Processing

### Available Functions

| Function | Description |
|---|---|
| `num2text` | Convert int/decimal number to Khmer word representation. |

### Function Details

<details>
<summary><strong><code>num2text()</code></strong></summary>

Convert int/decimal number to Khmer word representation.

| Parameter | Type | Description |
|---|---|---|
| `num` | `Union[int, float]` | Number to convert to text. |
| `style` | `Literal["normal", "3"] = "normal"` | The style of reading number that will use to convert to text. |
| `is_split` | `bool = False` | If True, the return will be a list of text in each digit. |

| Type | Description |
|---|---|
| `Union["str", "list[str]"]` | Output of Khmer transcripted text. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.number import num2text

print(num2text(100123))
# មួយសែនមួយរយម្ភៃបី
print(num2text(100123, style="3"))
# មួយរយពាន់មួយរយម្ភៃបី
print(num2text(100123, is_split=True))
# ['មួយ', 'សែន', 'មួយ', 'រយ', 'ម្ភៃ', 'បី']

print(num2text(10.0123))
# ដប់ចុចសូន្យមួយរយម្ភៃបី
print(num2text(1231.34))
# មួយពាន់ពីររយសាមសិបមួយចុចសាមសិបបួន
```
---
</details>


<br>

# Commoncrawl Processing

Provides feature to work with the scrapping/crawling content.
It could be serve as first stage data checking and grouping for further processing.

### Available Functions

| Function | Description |
|---|---|
| `quality_warning` | Web crawling context quality checking. |
| `document_filtering` | Classify warning into 3 levels of quality and filtered. |
| `is_adult_url_filter` | Classify URL as adult URL or not. |


### Function Details
<details>
<summary><strong><code>quality_warning()</code></strong></summary>

Web crawling context quality checking. Get all quality warning from the context.

**Noted:** There are predefined five warning flags.
- noisy: Ratio of Khmer_char/total_char > 0.5
- tiny: Contain less than or equal to 5 lines
- short_sentence: count of line with less then 100 char/total lines > 0.5
- header: top 20% of lines are short_sentence
- footer: bottom 20% of lines is short_sentence

| Parameter | Type | Description |
|---|---|---|
| `context` | `str` | Text for checking. |

| Return Type | Description |
|---|---|
| `list[str]` | List of warning flags. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.commoncrawl import check_quality_warning

text = """លោក តាន់ ហ្សង់ហ្វ្រង់ស្វ័រ៖ កម្ពុជាគង់តែស្គាល់ភាពរុងរឿងដូចសិង្ហបុរី បើរក្សាបានសន្តិភាព ស្ថិរភាព និងប្រឹងប្រែងអភិវឌ្ឍសេដ្ឋកិច្ច (Video inside)
Search ...
FRESH NEWS+ Home Local World Business KnowledgeAnalysis Youtube English Chinese (中文)
លោក តាន់ ហ្សង់ហ្វ្រង់ស្វ័រ៖ កម្ពុជាគង់តែស្គាល់ភាពរុងរឿងដូចសិង្ហបុរី បើរក្សាបានសន្តិភាព ស្ថិរភាព និងប្រឹងប្រែងអភិវឌ្ឍសេដ្ឋកិច្ច (Video inside)
2024-06-19 07:08pm
(ភ្នំពេញ)៖ លោក តាន់ ហ្សង់ហ្វ្រង់ស្វ័រ រដ្ឋមន្ត្រីប្រតិភូអមនាយករដ្ឋមន្ត្រី បានលើកឡើងថា កម្ពុជាគង់តែស្គាល់ភាពរុងរឿងដូចសិង្ហបុរីសព្វថ្ងៃ ប្រសិនបើរក្សាបានសន្តិភាព ស្ថិរភាព និងប្រឹងប្រែងអភិវឌ្ឍសេដ្ឋកិច្ចទៅមុខជាបន្តបន្ទាប់។"""

print(check_quality_warning(text))
# ['header', 'footer', 'short_sentences']
```
---
</details>

<details>
<summary><strong><code>is_adult_url_filter()</code></strong></summary>

Check if the url are appropriate content.

| Parameter | Type | Description |
|---|---|---|
| `url` | `str` | url string to check for keyword. |

| Return Type | Description |
|---|---|
| `bool` | True if the url content keyword, vise versa. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.commoncrawl.doc_filtering import is_adult_url_filter

print(is_adult_url_filter("https://bizkhmer.com/articles/18357"))
# false
print(is_adult_url_filter("https://example.phimsexnh.testing/category"))
# true
```
---
</details>


<details>
<summary><strong><code>document_filtering()</code></strong></summary>

Classify and filter those not match in quality.

| Parameter | Type | Description |
|---|---|---|
| `obj` | `dict` | Document dict object. |
| `quality_type` | `Literal["High", "Medium", "Low"] = "High"` | Quality level to keep. |

| Return Type | Description |
|---|---|
| `bool` | True if the url content keyword, vise versa. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.commoncrawl.doc_filtering import is_adult_url_filter

print(is_adult_url_filter("https://bizkhmer.com/articles/18357"))
# false
print(is_adult_url_filter("https://example.phimsexnh.testing/category"))
# true
```
---
</details>

<br>

# Deduplication

Deduplication utilities and similarity matching tools for removing
duplicate records, filtering redundant samples, and maintaining
dataset quality.

## URL Deduplicator

This module is for work with big data to avoid heavy check of exact match. 
It also support parallel running process.

**Note:** This module will be update to class/object base operation in the next version.

### Available Functions

| Function | Description |
|---|---|
| `is_url_duplicate` | Remove exact duplicate records based on identical url hashing. |
| `load_hashes_file` | Load stored URL hash fingerprints from a hash index file into memory. |
| `write_hash_file` | Persist URL hash fingerprints to a hash index file for future deduplication checks. |
<!-- | `is_url_duplicate` | Detect near-duplicate entries using text similarity matching. |
| `MinHashDeduplicator` | Efficient large-scale deduplication using MinHash signatures. |
| `SemanticDeduplicator` | Remove semantically similar samples using embedding similarity. |
| `deduplicate_dataset` | Execute dataset-wide deduplication pipeline with configurable strategy. |
| `compute_similarity` | Compute similarity score between two records or documents. |
| `filter_duplicates` | Filter duplicated entries from iterable datasets or file sources. |
| `generate_signature` | Generate hash or fingerprint signatures for dataset records. | -->

### Function Details


<details>
<summary><strong><code>is_url_duplicate()</code></strong></summary>

Check for duplication. if url not found, indexing it.

| Parameter | Type | Description |
|---|---|---|
| `url` | `str` | URL string. |
| `rt_hash` | `bool = False` | if true return url hash. |

| Return Type | Description |
|---|---|
| `bool` | True if the URL already seen before, false if URL have not seen yet. |
| `set(bool, url_hash)` | return set of URL seen status and its hash value. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.deduplicate.url_dedup import is_url_duplicate

list_urls = [
    "example.com",
    "example1.com",
    "example.com"
]

for url in list_urls:
    print(is_url_duplicate(url))
# False
# False
# True
```
---
</details>


<details>
<summary><strong><code>load_hashes_file()</code></strong></summary>

Load previous URL run footprint.

| Parameter | Type | Description |
|---|---|---|
| `path` | `str` | URL footprint cache. set default to '.cache/seen_url.txt' if not specify. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.deduplicate.url_dedup import is_url_duplicate, load_hashes_file

load_hashes_file()

list_urls = [
    "example.com",
    "example1.com",
    "example.com"
]

for url in list_urls:
    print(is_url_duplicate(url))
```
---
</details>

<details>
<summary><strong><code>write_hash_file()</code></strong></summary>

Save URL footprint for later check or run.

| Parameter | Type | Description |
|---|---|---|
| `path` | `str` | URL footprint cache. set default to '.cache/seen_url.txt' if not specify. |

<strong>Example</strong>

```python
from khmer_nlp_toolkits.deduplicate.url_dedup import write_hash_file


list_urls = [
    "example.com",
    "example1.com",
    "example.com"
]

for url in list_urls:
    print(is_url_duplicate(url))

write_hash_file()
```
---
</details>

## Document Deduplicator

This module are for identifying any exact match duplicated text or near duplicated text working with big data.

**NOTE:** Detail usage will be update later.


<br>

# Utility Functions

Utility helpers and workflow tools for dataset processing,
file handling, and pipeline execution.

### Available Functions

| Function | Description |
|---|---|
| `Pipeline` | Pipelines class execute processing in sequential or parallel mode. |
| `lazy_read_jsonl` | Lazily read `.jsonl` files line-by-line without load the whole data. |
| `count_file_line` | Count the number of lines in a file. |
| `get_filepath` | Retrieve absolute file paths from directories. |


### Function Details

<details>
<summary><strong><code>Pipeline</code></strong></summary>

Pipeline class for building sequential processing workflows.

This class allows chaining multiple functions into a reusable
end-to-end execution pipeline.

- Functions are executed sequentially.
- Output from the previous function is passed into the next function.
- Additional keyword arguments can be attached to each pipeline step.
- Useful for NLP preprocessing and custom text workflows.


**Initialization**

```python
Pipeline()
```

---
**Class Methods**

| Method | Description |
|---|---|
| `add()` | Add processing function into pipeline in order. |
| `run()` | Execute all pipeline tasks sequentially. |
| `run_parallel()` | Execute all pipeline tasks sequentially with data parallel running. |
| `get_queue_status()` | [For parallel run] Return current queue capacity status.<ul><li>Pipeline: <code>in_q -> s1 -> q1 -> s2 -> q2 -> s3 -> out_q</code> (4 queues total)</li><li>Example result: <code>[10, 10, 9, 0]</code> (<code>qsize=10</code>)</li><li>Most batches are stuck at step 3 (<code>s3</code>) because it processes slower than other steps.</li></ul> |

**Class Method Details**

<details>
<summary><strong><code>add()</code></strong></summary>
Add a processing function into the pipeline.

| Parameter | Type | Description |
|---|---|---|
| `step` | `Callable` | Processing function to append into pipeline. |
| `desc` | `str \| None` | Optional pipeline step description. |
| `step_params` | `Any` | Keyword arguments pre-passed into the function during execution. |
| `num_process` | `int = 1` | [For parallel run] Number of parallel processer config to spawn solely to run/perform this setup step. Increase this number for the step that do heavy work and take a lot of time for each batch running. |
| `is_wrap` | `bool = False` | [For parallel run] Set to true to wraped func in loop to execute as a batch. If False the data will pass to function directly. |

---
```python
from khmer_nlp_toolkits.pipeline import Pipeline


# Example custom function
def func_a(text: str, is_upper: bool = False) -> str:
    return text.upper() if is_upper else text.lower()

def func_b(text: str, times: int = 1) -> str:
    return text * times

# Create the pipeline
pipeline = Pipeline()

# Add functions into pipeline
pipeline.add(func_a, is_upper=True, desc="lower or upper text.")
pipeline.add(func_b, times=3)

# List functions inside pipeline
print(str(pipeline))
# ==============================
# All function flow in pipeline.
# ==============================
# 1. func_a(is_upper=True)
# 	lower or upper text.
# 2. func_b(times=3)
```
---
</details>

<details>
<summary><strong><code>run()</code></strong></summary>
Execute all pipeline functions sequentially.

| Parameter | Type | Description |
|---|---|---|
| `data` | `Any` | Input pipeline data. |

| Return Type | Description |
|---|---|
| `Any` | Result of last step in pipeline. |

---
```python
from khmer_nlp_toolkits.pipeline import Pipeline


# Example custom function
def func_a(text: str, is_upper: bool = False) -> str:
    return text.upper() if is_upper else text.lower()

def func_b(text: str, times: int = 1) -> str:
    return text * times

# Create the pipeline
pipeline = Pipeline()

# Add functions into pipeline
pipeline.add(func_a, is_upper=True, desc="lower or upper text.")
pipeline.add(func_b, times=3)

# Run pipeline in linear
INPUT_TEXT = "hello world"

output_text = pipeline.run(INPUT_TEXT)

print(output_text)
# HELLO WORLDHELLO WORLDHELLO WORLD
```
---
</details>

<details>
<summary><strong><code>run_parallel()</code></strong></summary>
Data and State parallel processing function. This function use multiprocesser and threading to execute data in parallel. Each state have a number of process to run independently on prarallel when data are available.

| Parameter | Type | Description |
|---|---|---|
| `data` | `Union[list, Iterator]` | Data to process. It must be a list or Iterator, since the data being processed in chuck of batch_size. |
| `batch_size` | `int = 100` | Number of data being processed per batch at a time. |
| `timeout` | `int = 30` | Maximum time to wait (in seconds) for data to be returned from the pipeline. If exceed the timeout, the process will end. This is to prevent logic break of Endless loop for waiting. |
| `qsize` | `int = 10` | Queue capacity. One queue slot equal to one batch data. If the queue full, the process corresponding to that queue will be on halt until next state process pickup batch to free queue. |

| Return Type | Description |
|---|---|
| `Any` | Result of last step in pipeline. |
---

```python
from khmer_nlp_toolkits.pipeline import Pipeline

# Example custom function
def func_a(text: str, is_upper: bool = False) -> str:
    return text.upper() if is_upper else text.lower()

def func_b(text: str, times: int = 1) -> str:
    return text * times

# Create the pipeline
pipeline = Pipeline()

# Add functions into pipeline
pipeline.add(func_a, is_wrap=True, is_upper=True, desc="lower or upper text.")
pipeline.add(func_b, is_wrap=True, times=2, num_process=1)    # there are 2 workers to do this job. Meaning 2 batches data are being process in parallel. 

# Run pipeline in linear
INPUT_TEXT = ["hello", "world", "Hi", "Bonjour", "Alo"]

# Consume data as soon as the batch finish.
for result in pipeline.run_parallel(INPUT_TEXT, batch_size=2):
    print(result)
# ['HELLOHELLO', 'WORLDWORLD']
# ['HIHI', 'BONJOURBONJOUR']
# ['ALOALO']

# Waiting until all data are finished.
print(list(pipeline.run_parallel(INPUT_TEXT, batch_size=2)))
# [['HELLOHELLO', 'WORLDWORLD'], ['HIHI', 'BONJOURBONJOUR'], ['ALOALO']]
```
</details>

---
</details>


<details>
<summary><strong><code>lazy_read_jsonl()</code></strong></summary>

Lazy read json from jsonline file. Consume data line-by-line with generator when called.

| Parameter | Type | Description |
|---|---|---|
| `filepath` | `str` | Jsonl file path. |
| `allow_none` | `bool = True` | Allow none object to pass through without raising error. |
| `limit` | `int = none` | Cut-off reading when the amount are meet. |
| `show_progress` | `bool = False` | Show tqdm progress bar. |

| Return Type | Description |
|---|---|
| `iteration` | Iteration object that can be consume. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.utils import lazy_read_jsonl

# Direct consume
for obj in lazy_read_jsonl(FILE_PATH):
    print(obj)

reader = lazy_read_jsonl(FILE_PATH)
print(next(reader))
# print result of first obj
print(len(reader))
# Given the remaining amount of data after consume.
```
---
</details>

<details>
<summary><strong><code>count_file_line()</code></strong></summary>

Given the total line within a file. This function does not read data from file, it use sub-process to execute linux command for memory efficient count.

| Parameter | Type | Description |
|---|---|---|
| `filepath` | `str` | Jsonl file path. |

| Return Type | Description |
|---|---|
| `int` | Total number of lines. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.utils import count_file_line

count = count_file_line(FILE_PATH)

print(count)
# Total number of lines
```
---
</details>

<details>
<summary><strong><code>get_filepath()</code></strong></summary>

Retrieves and sorts relative file paths from a source directory, optionally mapping them to a destination.

If a destination is provided, it ensures the directory exists and returns a list
of tuples containing (source_path, destination_path). Otherwise, it returns
a list of full paths to the files in the source directory.

| Parameter | Type | Description |
|---|---|---|
| `source` | `str` | The directory path to scan for files. |
| `destination` | `str, optional` | The directory path where files are intended to be mapped or moved. Defaults to None.. |

| Return Type | Description |
|---|---|
| `list` | A list of strings (source paths) if destination is None. |
| `list[tuple]` | A list of (source_path, destination_path) pairs if destination is provided. |


<strong>Example</strong>

```python
from khmer_nlp_toolkits.utils import get_filepath

# filepath = get_filepath(FILE_PATH)
filepath = get_filepath("docs/")
print(filepath)
# ['doc/file1.jsonl', 'doc/file2.jsonl', ...]

filepath = get_filepath("docs/", "abc/abc")
print(filepath)
# [
#   ('doc/file1.jsonl', 'abc/abc/file1.jsonl'),
#   ('dir/file2.jsonl', 'abc/abc/file2.jsonl'),
#   ...
# ]
```
---
</details>




# References
<a id="ref-1"></a>
[[1]](https://aclanthology.org/2025.coling-main.87/) Hour Kaing, Raj Dabre, Haiyue Song, Van-Hien Tran, Hideki Tanaka, and Masao Utiyama. 2025. PrahokBART: A Pre-trained Sequence-to-Sequence Model for Khmer Natural Language Generation. In Proceedings of the 31st International Conference on Computational Linguistics, pages 1309–1322, Abu Dhabi, UAE. Association for Computational Linguistics.

<a id="ref-2"></a>
[[2]](https://www.unicode.org/L2/L2022/22290-khmer-encoding.pdf) Martin Hosken, Norbert Lindenberg, and Makara Sok. 2022. Khmer encoding structure. Technical report, The Unicode Technical Committee.

<a id="ref-3"></a>
[3] Hoang, P. V. (2020). Khmer Natural Language Processing Toolkit. GitHub repository. https://github.com/VietHoang1512/khmer-nltk

<a id="ref-4"></a>
[4] Vichet Chea, Ye Kyaw Thu, Chenchen Ding, Masao Utiyama, Andrew Finch, and Eiichiro Sumita. Khmer word segmentation using conditional random fields. Khmer Natural Language Processing, 2015

