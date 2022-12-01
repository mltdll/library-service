import stripe
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from stripe.error import InvalidRequestError

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(borrowing__user=self.request.user.id)


@api_view(["GET"])
def cancel_view(request: Request) -> Response:
    stripe.api_key = settings.STRIPE_API_KEY

    session_id = request.query_params.get("session_id")
    try:
        stripe.checkout.Session.retrieve(session_id)
    except InvalidRequestError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def success_view(request: Request, borrowing_pk) -> Response:
    stripe.api_key = settings.STRIPE_API_KEY

    session_id = request.query_params.get("session_id")
    try:
        stripe.checkout.Session.retrieve(session_id)
    except InvalidRequestError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    payment = Payment.objects.get(borrowing__pk=borrowing_pk)
    payment.status_payment = "PA"
    payment.save()

    return Response(status=status.HTTP_200_OK)

