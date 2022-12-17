from django.contrib import admin

from .models import Room, Amenity


# 진짜 사용할땐 common에 만들자
@admin.action(description="Set all prices to 0")
def reset_prices(model_admin, request, queryset):
    # print(model_admin)  # 이 액션을 적용한 어드민 클래스
    # print(request)  # 해당 요청에 대한 정보
    # print(dir(request))
    # print(request.user)  # 요청한 유저의 정보
    # print(queryset)  # 해당 액션을 적용한 모델의 쿼리셋, 어드맨 패널에서의 row
    for qs in queryset.all():
        qs.price = 0
        qs.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    actions = (reset_prices,)

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
    # search_fields는 기본적으로 유저가 입력한 값이 포함된 모든 결과를 보여줌 (__contains)
    search_fields = (
        "name",  # 시작하는 값만 보여줌 (__startswith)
        "=price",  # 정확히 일치하는 값만 보여줌 (__exact)
        # "price__exact" 이러면 갑자기 입력값을 int로 바꾸더라?
        "owner__username",  # 외래키를 통해 검색할때는 __를 사용 (^, = 등 사용가능)
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
