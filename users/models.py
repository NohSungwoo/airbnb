from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("usd", "Dollar")

    profile_photo = models.URLField(
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices,
    )
