from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from book.models import Book
from borrowing.models import Borrowing


class BorrowingTest(TestCase):
    def setUp(self) -> None:
        self.book = Book.objects.create(
            title="test_title1",
            author="test_author1",
            cover="hard",
            inventory=1,
            daily_fee=10,
        )
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345"
        )

    def test_create_borrowing_with_incorrect_data(self):
        try:
            self.book.inventory = 0
            self.book.save()
            Borrowing.objects.create(
                expected_date="2022-12-26",
                book_id=1,
                user=self.user
            )
        except ValidationError:
            pass
        else:
            raise AssertionError("Borrowing can't have book with 0 inventory")

    def test_borrowing_cant_have_expected_date_lower_then_now(self):
        try:
            Borrowing.objects.create(
                expected_date="2022-10-26",
                book=self.book,
                user=self.user
            )
        except ValidationError:
            pass
        else:
            raise AssertionError("Expected date can't be lower than actual")
