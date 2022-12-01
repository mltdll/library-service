from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book
from book.serializers import BookSerializer


def create_books():
    Book.objects.create(
        title="test_title1",
        author="test_author1",
        cover="hard",
        inventory=10,
        daily_fee=10,
    )
    Book.objects.create(
        title="test_title2",
        author="test_author2",
        cover="soft",
        inventory=20,
        daily_fee=20,
    )


class BookApiPublicTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        create_books()

    def test_get_book(self):
        books = self.client.get("/api/book/books/")
        serializer = BookSerializer(Book.objects.all(), many=True)

        self.assertEqual(books.status_code, status.HTTP_200_OK)
        self.assertEqual(books.data, serializer.data)

    def test_get_book_details(self):
        book = self.client.get("/api/book/books/1/")
        serializer = BookSerializer(get_object_or_404(Book, id=1))

        self.assertEqual(book.status_code, status.HTTP_200_OK)
        self.assertEqual(book.data, serializer.data)

    def test_get_invalid_book(self):
        book = self.client.get("/api/book/books/34/")

        self.assertEqual(book.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_book(self):
        book = self.client.post(
            "/api/book/books/",
            {
                "title": "test_title2",
                "author": "test_author2",
                "cover": "SOFT",
                "inventory": 20,
                "daily_fee": 20,
            },
        )

        self.assertEqual(book.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_movie(self):
        book = self.client.put(
            "/api/book/books/",
            {
                "title": "test_title2",
                "author": "test_author2",
                "cover": "SOFT",
                "inventory": 20,
                "daily_fee": 20,
            },
        )

        self.assertEqual(book.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book(self):
        book = self.client.delete(
            "/api/book/books/1/"
        )

        self.assertEqual(book.status_code, status.HTTP_401_UNAUTHORIZED)


class BookApiStaffUserTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@admin.com",
            "admin123"
        )
        self.client.force_authenticate(user=self.user)
        create_books()

    def test_post_book(self):
        book = self.client.post(
            "/api/book/books/",
            {
                "title": "test_title3",
                "author": "test_author3",
                "cover": "hard",
                "inventory": 30,
                "daily_fee": 30,
            },
        )

        self.assertEqual(book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_movie(self):
        book = self.client.put(
            "/api/book/books/1/",
            {
                "title": "test_title2",
                "author": "test_author2",
                "cover": "soft",
                "inventory": 20,
                "daily_fee": 20,
            },
        )

        self.assertEqual(book.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        book = self.client.delete(
            "/api/book/books/1/"
        )

        self.assertEqual(book.status_code, status.HTTP_204_NO_CONTENT)
