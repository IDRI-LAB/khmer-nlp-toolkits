# khmer_nlp_toolkits

Khmer NLP Toolkits is an open-source Python library that provides practical utilities, text processing functions, and NLP components for the Khmer language.

The project is designed to make Khmer NLP easier for:
- Researchers
- Students
- Developers
- Production systems
- AI applications

It aims to provide a unified, lightweight, and extensible toolkit for common Khmer language processing tasks.

<br>

# Installation
### Requirements
- Python 3.10+

### Install from PyPI
```bash
pip install khmer_nlp_toolkits
```

<br>

# Quick Start
```python
from khmer_nlp_toolkits.text import *
from khmer_nlp_toolkits.number import num2text

print(num2text(2026))
# ពីរពាន់ម្ភៃប្រាំមួយ

print(anonymizer(("You can contact us by phone at +855 12 345 678, email us at support@example.com, "
"or visit our website at https://www.example.com anytime.")))
# You can contact us by phone at [TEL], email us at [EML], or visit our website at [URL] anytime.

print(text_cleaner(
    "\u200b&nbsp;Hello\u2014\u2014World!!!??      ខ្មែរ   123\u200b&nbsp;"
))
# "Hello - World !? ខ្មែរ 123"
```

<br>

# Features

Khmer NLP Toolkits provides modular utilities and NLP components for Khmer language processing.

### Commoncrawl [🔗](docs/usage.md)

- Content Quality Warning
- Document Quality Filtering
- Adult Content Filtering

### Text Processing [🔗](docs/usage.md)

- Text Anonymization
- Text Normalization
- Text Cleaning
- Segmentation

### Number Processing [🔗](docs/usage.md)

- number conversion to text

### Deduplication [🔗](docs/usage.md)

- URL deduplication
- Content Deduplication

### Utilities [🔗](docs/usage.md)

- End2End Pipeline
- File Utilities Features

<br>

# Vision

The long-term goal of Khmer NLP Toolkits is to help build a comprehensive open-source ecosystem for Khmer Natural Language Processing and accelerate Khmer AI/NLP research and development.

We hope this project can contribute to:
- Better Khmer language tooling
- Educational resources
- NLP research accessibility
- Open-source AI infrastructure for Khmer

<br>

# Contributing

Contributions, issues, and feature requests are welcome. Feel free to open a pull request or discussion.

### Planned Features
- [ ] Khmerize
- [ ] NER
- [ ] Semantic Similarity
- [ ] Text2Num
- [ ] etc.khmer_nlp_toolkits/transliterate/romanize.py


<br>

# Contributors

- [Sopagna HEANG](https://github.com/pagna-kun)
- [Natt KORAT](https://nattkorat.github.io/)
- [Chily RAN](https://github.com/ChilyRan)

<br>

# License

This project is licensed under the MIT License.

<br>

# References
<a id="ref-1"></a>
[[1]](https://aclanthology.org/2025.coling-main.87/) Hour Kaing, Raj Dabre, Haiyue Song, Van-Hien Tran, Hideki Tanaka, and Masao Utiyama. 2025. PrahokBART: A Pre-trained Sequence-to-Sequence Model for Khmer Natural Language Generation. In Proceedings of the 31st International Conference on Computational Linguistics, pages 1309–1322, Abu Dhabi, UAE. Association for Computational Linguistics.

<a id="ref-2"></a>
[[2]](https://www.unicode.org/L2/L2022/22290-khmer-encoding.pdf) Martin Hosken, Norbert Lindenberg, and Makara Sok. 2022. Khmer encoding structure. Technical report, The Unicode Technical Committee.

<a id="ref-3"></a>
[3] Hoang, P. V. (2020). Khmer Natural Language Processing Toolkit. GitHub repository. https://github.com/VietHoang1512/khmer-nltk

<a id="ref-4"></a>
[4] Vichet Chea, Ye Kyaw Thu, Chenchen Ding, Masao Utiyama, Andrew Finch, and Eiichiro Sumita. Khmer word segmentation using conditional random fields. Khmer Natural Language Processing, 2015

