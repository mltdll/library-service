from datetime import date

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_q.tasks import async_task
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import BorrowSerializer, ReadBorrowSerializer


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.prefetch_related("book")
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadBorrowSerializer

        return BorrowSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        async_task(
            "notification_service.notify.notify_borrowing_created", borrowing
        )


@api_view(["GET"])
def success_payment(request, pk):
    borrow = get_object_or_404(Borrowing, id=pk)

    if not borrow.actual_return_date:
        borrow.actual_return_date = date.today()
        borrow.book.inventory += 1
        borrow.book.save()
        borrow.save()

    serializer = BorrowSerializer(borrow)

    return Response(serializer.data)
