from django.db import transaction
from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from payment.serializers import PaymentSerializer


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("id", "user", "actual_return_date")

    def validate(self, attrs):
        data = super(BorrowSerializer, self).validate(attrs)

        book = attrs["book"]

        Borrowing.validate_book(book.inventory, serializers.ValidationError)

        return data

    @transaction.atomic
    def create(self, validated_data):
        instance = Borrowing.objects.create(**validated_data)
        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        return instance


class ReadBorrowSerializer(BorrowSerializer):
    book = BookSerializer()
    payment = PaymentSerializer()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_date",
            "actual_return_date",
            "book",
            "user",
            "payment",
        )
