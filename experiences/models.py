from django.db import models

import users.models
from common.models import CommonModel


class Experience(CommonModel):
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    name = models.CharField(max_length=250)
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey(
        "categories.Category",
        related_name="experiences",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    explanation = models.TextField()

    def __str__(self):
        return self.name
