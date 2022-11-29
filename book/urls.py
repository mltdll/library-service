from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookList.as_view()),
    path("books/", views.BookListCreate.as_view()),
    path("books/<int:pk>", views.BookRetrieveUpdateDestroy.as_view()),
]

app_name = "book"
