from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowViewSet, success_payment

router = routers.DefaultRouter()
router.register("borrowings", BorrowViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("success/<int:pk>/", success_payment)
]

app_name = "borrowing"
