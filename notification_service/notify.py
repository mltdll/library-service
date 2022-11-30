import os

import requests

from borrowing.models import Borrowing

API_URL = "https://api.telegram.org/bot"
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_CHAT_ID = os.environ["CHAT_ID"]


def send_message(bot_token: str, chat_id: str, text: str) -> int:
    api_method = "/sendMessage"
    full_url = f"{API_URL}{bot_token}{api_method}"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.get(full_url, json=payload)

    return response.status_code


def notify_borrowing_created(borrowing: Borrowing) -> int:
    user = borrowing.user

    message = (
        f"User {user.email} (id={user.id}) created a new borrowing:\n\n"
        f"Book: {borrowing.book}\n"
        f"Date: {borrowing.borrow_date}\n"
        f"Date due: {borrowing.expected_date}\n"
    )

    return send_message(BOT_TOKEN, ADMIN_CHAT_ID, message)
