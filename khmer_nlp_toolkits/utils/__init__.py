"""
Simple utilities support feature for fast development.
"""
from khmer_nlp_toolkits.utils.file_utils import lazy_read_jsonl, get_filepath, count_file_line
from khmer_nlp_toolkits.utils.telegram_notif import sent_msg as sent_telegram_msg


__all__ = [
    "lazy_read_jsonl",
    "get_filepath",
    "count_file_line",
    "sent_telegram_msg"
]
