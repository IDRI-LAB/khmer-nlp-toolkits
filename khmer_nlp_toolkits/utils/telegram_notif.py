"""
Module working with Telegram bot
"""
import logging
import requests
from dotenv import dotenv_values

ENV = dotenv_values()
TOKEN = ENV["TELE_TOKEN"]
CHAT_ID = ENV["TELE_CHAT_ID"]


def sent_msg(msg, script_name = ""):
    """
    log message in console and sent to telegram channel.

    Parameters
    ----------
    msg: str
        Message to log.
    script_name: str
        Script title.
    """
    if script_name:
        msg = (
            f"<u><b>SCRIPT: {script_name}</b></u>\n\n"
            f"{msg}"
        )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=HTML"
    logging.info(msg)
    try:
        requests.post(url, timeout=15)
    except requests.exceptions.RequestException as error:
        logging.error("Telegram bot: %s", error)


if __name__ == "__main__":
    message = (
        "Report: Test msg!!\n"
        f"- Items processed: \n"
        f"- Errors: \n"
    )
    sent_msg(message)