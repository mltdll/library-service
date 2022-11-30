from django.urls import path
from .views import BorrowingListView, BorrowingRetrieveView

urlpatterns = [
    path("", BorrowingListView.as_view()),
    path("<int:pk>/", BorrowingRetrieveView.as_view()),
]

app_name = "borrowing"
