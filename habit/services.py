import requests

from config.settings import TG_URLS, TELEGRAM_API_KEY


def send_tg_message(chat_id, message):
    params = {
        'text': message,
        'chat_id': chat_id,

    }
    requests.get(f'{TG_URLS}{TELEGRAM_API_KEY}/sendMessage', params=params)
