from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Now

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrows"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrows"
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(borrow_date__lte=Now()),
                name="check_borrow_date",
            ),
            CheckConstraint(
                check=Q(expected_date__gt=Now()),
                name="check_expected_return_date",
            ),
            CheckConstraint(
                check=Q(actual_return_date__gt=Now()),
                name="check_actual_return_date",
            ),
        ]

    @staticmethod
    def validate_book(inventory: int, error_to_raise) -> None:
        if inventory < 1:
            raise error_to_raise("We don't have this book in stock")

    def clean(self) -> None:
        Borrowing.validate_book(self.book.inventory, ValidationError)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.full_clean()
        return super(Borrowing, self).save(force_insert, force_update, using, update_fields)
