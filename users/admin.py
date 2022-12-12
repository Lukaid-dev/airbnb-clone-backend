from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            # admin에서 section을 나눌 수 있음
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "email",
        "name",
        "is_host",
    )
    list_display_links = (
        "id",
        "username",
    )
