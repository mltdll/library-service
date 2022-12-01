import stripe
from django.conf import settings

from borrowing.models import Borrowing

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_session(borrowing: Borrowing) -> stripe.checkout.Session:
    book = borrowing.book

    delta = borrowing.actual_return_date - borrowing.borrow_date
    days = delta.days
    total_price_cents = days * book.daily_fee * 100

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

        # TODO: implement urls
        success_url="http://localhost:8000/api/payment/success",
        cancel_url="http://localhost:8000/api/payment/cancel",
    )
