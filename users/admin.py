from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "profile_photo",
                    "name",
                    "password",
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                ),
                "classes": ("wide",),
            },
        ),
    )
    list_display = (
        "name",
        "is_host",
    )
