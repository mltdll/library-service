import datetime
import os

import requests
from django.conf import settings

from borrowing.models import Borrowing

API_URL = "https://api.telegram.org/bot"
BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
ADMIN_CHAT_ID = settings.TELEGRAM_CHAT_ID


def send_message(bot_token: str, chat_id: str, text: str) -> int:
    """
    Send a message through a Telegram bot.
    """
    api_method = "/sendMessage"
    full_url = f"{API_URL}{bot_token}{api_method}"
    payload = {"chat_id": chat_id, "text": text}

    response = requests.get(full_url, json=payload)

    return response.status_code


def notify_borrowing_created(borrowing: Borrowing) -> int:
    """
    Send a notification about borrowing creation to the admin chat.
    """

    user = borrowing.user

    message = (
        f"User {user.email} (id={user.id}) created a new borrowing:\n\n"
        f"Book: “{borrowing.book}” by {borrowing.book.author}\n"
        f"Date created: {borrowing.borrow_date}\n"
        f"Date due: {borrowing.expected_date}"
    )

    return send_message(BOT_TOKEN, ADMIN_CHAT_ID, message)


def notify_overdue_borrowings() -> None:
    """
    Send a message for each overdue borrowing to the admin chat.
    If no such borrowings exist, send "No borrowings overdue today!".
    """
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    overdue_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True, expected_date__lte=tomorrow
    ).select_related("book")

    if not overdue_borrowings.exists():
        send_message(BOT_TOKEN, ADMIN_CHAT_ID, "No borrowings overdue today!")
        return

    for borrowing in overdue_borrowings:
        user = borrowing.user

        # I don't think it makes sense to create a template for messages here
        # and in notify_borrowing_created(), since they may have to be
        # changed independently.
        message = (
            f"User {user.email} (id={user.id}) has an overdue borrowing:\n\n"
            f"id: {borrowing.id}\n"
            f"Book: “{borrowing.book}” by {borrowing.book.author}\n"
            f"Date created: {borrowing.borrow_date}\n"
            f"Date due: {borrowing.expected_date}"
        )
        send_message(BOT_TOKEN, ADMIN_CHAT_ID, message)
