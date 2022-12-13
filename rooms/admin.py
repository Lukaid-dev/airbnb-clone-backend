from django.contrib import admin

from .models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    list_display = (
        "id",
        "name",
        "price",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_filter = (
        "country",
        "city",
        "kind",
        "pet_friednly",
        "amenities",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """Amenity Admin Definition"""

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
