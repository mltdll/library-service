from datetime import date
from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from django_q.tasks import async_task
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import BorrowSerializer, ReadBorrowSerializer
from payment.models import Payment
from payment.payment_sessions import create_stripe_session


def create_payment(borrowing: Borrowing):
    session = create_stripe_session(borrowing)

    # This is where price is located inside a session. Couldn't they make it
    # easier to find?
    price_cents = session.list_line_items()["data"][0]["amount_total"]

    price = Decimal(price_cents) / 100

    payment_data = {
        "status_payment": "PE",  # New payments are pending.
        "type_payment": "PA",  # Type of the payment is payment.
        "borrowing": borrowing,
        "session_url": session.url,
        "session_id": session.stripe_id,
        "money": price,
    }

    return Payment.objects.create(**payment_data)


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.prefetch_related("book")
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if self.request.user.is_staff:
            if user_id:
                queryset = queryset.filter(user=int(user_id))

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user.id)

        if is_active == "yes":
            queryset = queryset.filter(actual_return_date__isnull=True)

        if is_active == "no":
            queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadBorrowSerializer

        return BorrowSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)

        # It doesn't seem like the output of the task can be useful here.
        async_task(
            "notification_service.notify.notify_borrowing_created", borrowing
        )


@api_view(["GET"])
def return_borrowing_view(request, pk):
    borrowing = get_object_or_404(Borrowing, id=pk)

    if not borrowing.actual_return_date:
        with transaction.atomic():
            borrowing.actual_return_date = date.today()
            borrowing.book.inventory += 1
            borrowing.book.save()
            borrowing.save()

            create_payment(borrowing)

    serializer = BorrowSerializer(borrowing)

    return Response(serializer.data)
