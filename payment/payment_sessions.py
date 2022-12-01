import stripe
from django.conf import settings
from django.urls import reverse

from borrowing.models import Borrowing

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_session(borrowing: Borrowing) -> stripe.checkout.Session:
    book = borrowing.book

    delta = borrowing.actual_return_date - borrowing.borrow_date
    # Took a book and returned it the same day? Pay anyway!
    days = max(delta.days, 1)
    total_price_cents = int(days * book.daily_fee * 100)

    delta_overdue = borrowing.actual_return_date - borrowing.expected_date
    days_overdue = max(delta_overdue.days, 0)

    total_price_cents += int(days_overdue * book.daily_fee * 100)

    return stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": book.title,
                    },
                    "unit_amount": total_price_cents,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        # TODO: Yay, hardcoded localhost!
        success_url="http://127.0.0.1:8000"
        f"{reverse('payment:success', args=[borrowing.id])}"
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=f"http://127.0.0.1:8000{reverse('payment:cancel')}"
        "?session_id={CHECKOUT_SESSION_ID}",
    )
