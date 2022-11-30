from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "borrowing"
