from django_q.tasks import async_task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
