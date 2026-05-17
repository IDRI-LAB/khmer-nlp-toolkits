# khmer_nlp_toolkits

This project is aimed to build and assemble all functionality of Natuaral Language Processing Toolkits for Khmer language. 

# Features
- [x] Dynamic abstruct pipeline (linear & parallel running)

Commoncrawl Package
- [x] Document_filtering
    - [x] adult_url_filter
    - [x] doc_quality_classify (high, medium, low)

Deduplicate
- [x] url_deduplication
- [x] document_deduplication

Number Package
- [x] num2text (int2str)
- [ ] text2num

Text Package
- [ ] anaonymize
    - [x] TEL, EMAIL, URL
    - [ ] PII (name)
- [x] clean
    - [x] text_cleaner
    - [x] remove_invisible_chars
    - [x] remove_misc_symbols
    - [x] remove_repetitive_punc
    - [x] space_handler
    - [x] count_khmer_char
- [x] lang masking (replace unknown lanugage with special token)
- [x] normalizer
    - [x] english noramlise (NFDK + lowercase)
    - [x] khmer unicode ordering (SIL normalizer)
- [x] Segmentation
    - [x] Compound segmentation (Khmer-NLTK)
    - [x] Morpheme segmentation (CADT model)
    - [x] KCC segmentation (Rule-base)
    - [x] Sentence segmentation (Rule-base)
    - [x] Paragraph segmentation (Rule-base)

Utils package
- [x] telegram notif (real-time alert)
- [x] other file supporting function

Future features/model
- [ ] Part-of-Speech tagging
- [ ] Name entity recognition
- [ ] Text classification
- [ ] Next word prediction
- [ ] Word embedding


# Installation


# Usage