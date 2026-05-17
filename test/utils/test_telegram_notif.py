import pytest
import requests

from khmer_nlp_toolkits.utils.telegram_notif import sent_msg


def test_seng_msg(mocker):
    mock = mocker.patch("khmer_nlp_toolkits.utils.telegram_notif.requests.post")

    sent_msg("Hello msg ....", "Unittest")
    mock.assert_called_once()

    mock.side_effect = requests.exceptions.Timeout(
        "Connection timed out"
    )
    sent_msg("Hello msg ....", "Unittest")
    # mock.assert_called_once()
