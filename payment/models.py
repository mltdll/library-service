from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = (("PE", "PENDING"), ("PA", "PAID"))
    TYPE_CHOICES = (("PA", "PAYMENT"), ("FI", "FINE"))

    status_payment = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type_payment = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money = models.DecimalField(max_digits=5, decimal_places=2)
