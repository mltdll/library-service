from django_q.tasks import async_task
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from borrowing.models import Borrowing
from borrowing.serializers import BorrowSerializer, ReadBorrowSerializer


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
        async_task(
            "notification_service.notify.notify_borrowing_created", borrowing
        )
