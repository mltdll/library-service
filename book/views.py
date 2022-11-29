from rest_framework import generics, permissions
from .serializers import BookSerializer
from .models import Book


class BookList(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user).order_by("title")


class BookListCreate(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user).order_by("title")


class BookRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Book.objects.filter(user=user)
