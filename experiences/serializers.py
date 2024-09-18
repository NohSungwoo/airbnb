from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experience


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(read_only=True, many=True)
    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = (
            "pk",
            "country",
            "city",
            "name",
            "price",
            "address",
            "start",
            "end",
            "description",
            "host",
            "category",
            "perks",
        )
