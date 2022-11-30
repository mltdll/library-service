import os

import requests

API_URL = "https://api.telegram.org/bot"
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_CHAT_ID = os.environ["CHAT_ID"]


def send_message(bot_token: str, chat_id: int, text: str) -> int:
    api_method = "/sendMessage"
    full_url = f"{API_URL}{bot_token}{api_method}"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.get(full_url, json=payload)

    return response.status_code
