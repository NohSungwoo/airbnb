from django.db import models

from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reviews",
        null=True,
        on_delete=models.SET_NULL,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="reviews",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} / {self.rating}"
