from rest_framework import serializers

from book.models import Book
from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_date", "actual_return_date", "book", "user")
        read_only_fields = ("id", "user", "actual_return_date")

    def validate(self, attrs):
        data = super(BorrowSerializer, self).validate(attrs)

        book = Book.objects.get(id=attrs["book"].id)

        Borrowing.validate_book(book.inventory, serializers.ValidationError)

        """
        I don't know where i must do this
        """

        book.inventory -= 1
        book.save()

        return data


class BorrowDetailSerializer(BorrowSerializer):
    book = BookSerializer()
