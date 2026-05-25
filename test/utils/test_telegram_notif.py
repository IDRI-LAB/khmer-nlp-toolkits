import pytest
import requests

from khmer_nlp_toolkits.utils.telegram_notif import sent_msg


def test_seng_msg(mocker, monkeypatch):
    with pytest.raises(ValueError):
        sent_msg("Hello msg ....", "Unittest")

    mock = mocker.patch("khmer_nlp_toolkits.utils.telegram_notif.requests.post")
    monkeypatch.setattr("khmer_nlp_toolkits.utils.telegram_notif.TOKEN", "ExampleToken")
    monkeypatch.setattr("khmer_nlp_toolkits.utils.telegram_notif.CHAT_ID", "ExampleChatID")

    sent_msg("Hello msg ....", "Unittest")
    mock.assert_called_once()

    mock.side_effect = requests.exceptions.Timeout(
        "Connection timed out"
    )
    log_mock = mocker.patch("khmer_nlp_toolkits.utils.telegram_notif.logging.error")
    sent_msg("Hello msg ....", "Unittest")
    log_mock.assert_called_once()
