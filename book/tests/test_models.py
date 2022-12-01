from django.test import TestCase

from book.models import Book


class BookTests(TestCase):
    def test_books_str(self):
        book = Book.objects.create(
            title="test_title",
            author="test_author",
            cover="HARD",
            inventory=10,
            daily_fee=10
        )

        self.assertEqual(str(book), "test_title")
