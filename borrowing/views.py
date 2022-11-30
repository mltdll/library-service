from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(user=user).prefetch_related("book")


class BorrowingRetrieveView(generics.RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer

    def get_queryset(self):
        user = self.request.user

        return Borrowing.objects.filter(user=user).prefetch_related("book")
