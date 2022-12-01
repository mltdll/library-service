from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowViewSet, return_borrowing_view

router = routers.DefaultRouter()
router.register("borrowings", BorrowViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("return/<int:pk>/", return_borrowing_view)
]

app_name = "borrowing"
