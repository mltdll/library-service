from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.db.models.functions import Now

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField()
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )
    book = models.ManyToManyField(Book, blank=True, related_name="borrowings")

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(borrow_date__lte=Now()),
                name="check_borrow_date",
            ),
            CheckConstraint(
                check=Q(expected_return_date__gt=F("borrow_date")),
                name="check_expected_return_date",
            ),
            CheckConstraint(
                check=Q(actual_return_date__gt=F("borrow_date")),
                name="check_actual_return_date",
            ),
        ]

    def __str__(self):
        return f"{self.borrow_date} {self.expected_return_date} {self.actual_return_date}"
