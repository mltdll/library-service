from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentViewSet, cancel_view, success_view

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("success/<int:borrowing_pk>/", success_view, name="success"),
    path("cancel/", cancel_view, name="cancel"),
]


app_name = "payment"
