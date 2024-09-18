from rest_framework import serializers

from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "profile_photo",
            "username",
        )


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "id",
            "last_name",
            "first_name",
            "groups",
            "user_permissions",
        )
