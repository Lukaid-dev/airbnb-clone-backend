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
        "total_amenities",
        "rating",
        "owner",
        "created_at",
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

    # 모델과 어드민 모두에 같은 이름의 메서드가 어드민에선 어드민에 있는 메서드가 우선 적용
    # 모델에 정의할거면 여기저기 쓰이는거만 쓰자
    # def total_amenities(self, test):
    #     return test.amenities.count()

    def total_amenities(self, Room):
        return Room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """Amenity Admin Definition"""

    list_display = (
        "name",
        "description",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
