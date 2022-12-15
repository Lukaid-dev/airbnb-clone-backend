from django.contrib import admin

from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "host",
        "price",
        "start",
        "end",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_filter = ("category",)


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "detail",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
