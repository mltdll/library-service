from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    COVER_CHOICES = (
        ("hard", "HARD",),
        ("soft", "SOFT",)
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=64)
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True
    )

    def __str__(self):
        return self.title
