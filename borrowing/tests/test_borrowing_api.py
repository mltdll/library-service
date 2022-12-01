from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book
from borrowing.models import Borrowing


def sample_book() -> Book:
    return Book.objects.create(
                    title="test_title1",
                    author="test_author1",
                    cover="hard",
                    inventory=10,
                    daily_fee=10,
                )


def sample_user(email: str = "test@test.com", staff = False) -> get_user_model():
    return get_user_model().objects.create_user(
            email=email,
            password="test12345",
            is_staff=staff
        )


def sample_borrowing(book: Book, user: get_user_model()) -> Borrowing:
    return Borrowing.objects.create(
                expected_date="2022-12-26",
                book=book,
                user=user
            )


class BorrowingPublicApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = sample_book()
        self.user = sample_user()
        self.borrowing1 = sample_borrowing(self.book, self.user)
        self.borrowing2 = sample_borrowing(self.book, self.user)

    def test_anonymous_user_cant_see_borrowings(self):
        borrowings = self.client.get("/api/borrow/borrowings/")

        self.assertEqual(borrowings.data, [])

    def test_anonymous_cant_create_borrowing(self):
        borrowing = self.client.post(
            "/api/borrow/borrowings/",
            {
                "expected_date": "2022-12-26",
                "book": self.book,
                "user": self.user
            }
        )

        self.assertEqual(borrowing.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_cant_update_borrowing(self):
        borrowing = self.client.put(
            "/api/borrow/borrowings/1/",
            {
                "expected_date": "2022-12-26",
                "book": self.book,
                "user": self.user
            }
        )

        self.assertEqual(borrowing.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_cant_delete_borrowing(self):
        borrowing = self.client.post(
            "/api/borrow/borrowings/1/"
        )

        self.assertEqual(borrowing.status_code, status.HTTP_401_UNAUTHORIZED)


class BorrowingAuthenticatedTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = sample_book()
        self.user = sample_user()
        self.borrowing1 = sample_borrowing(self.book, self.user)
        self.borrowing2 = sample_borrowing(self.book, self.user)
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_see_only_his_borrows(self):
        new_user = sample_user("test2@test.com")
        sample_borrowing(sample_book(), new_user)
        borrows = self.client.get(
            "/api/borrow/borrowings/"
        )

        self.assertEqual(len(borrows.data), Borrowing.objects.filter(user=self.user).count())

    def test_authenticated_user_can_create_borrows(self):
        payload = {
            "expected_date": "2026-12-26",
            "book": 1
        }
        response = self.client.post(
            "/api/borrow/borrowings/",
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 3)

    def test_authenticated_user_can_update_borrows(self):
        payload = {
            "expected_date": "2026-12-12",
            "book": 1
        }
        response = self.client.put(
            "/api/borrow/borrowings/1/",
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["expected_date"], payload["expected_date"])

    def test_fiter_by_user_id(self):
        user2 = sample_user("new@test.com")
        book = sample_book()
        sample_borrowing(book, user2)
        sample_borrowing(book, user2)
        sample_borrowing(book, user2)
        sample_borrowing(book, user2)

        response = self.client.get(
            f"/api/borrow/borrowings/?user_id={user2.id}"
        )

        self.assertEqual(len(response.data), len(self.user.borrows.all()))


class BorrowingStaffTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = sample_book()
        self.user = sample_user(staff=True)
        self.borrowing1 = sample_borrowing(self.book, self.user)
        self.borrowing2 = sample_borrowing(self.book, self.user)
        self.client.force_authenticate(user=self.user)

    def test_fiter_by_user_id(self):
        user2 = sample_user("new@test.com")
        book = sample_book()
        sample_borrowing(book, user2)
        sample_borrowing(book, user2)
        sample_borrowing(book, user2)

        response = self.client.get(
            f"/api/borrow/borrowings/?user_id={user2.id}"
        )

        self.assertEqual(len(response.data), len(user2.borrows.all()))


