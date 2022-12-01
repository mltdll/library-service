from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly
from .serializers import BookSerializer
from .models import Book


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
