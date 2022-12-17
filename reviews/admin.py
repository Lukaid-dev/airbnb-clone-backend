from django.contrib import admin

from .models import Review


# 진짜 사용할땐 common에 만들자
class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(payload__contains=word)
        else:
            pass
        # if self.value() == "good":
        #     return queryset.filter(payload__contains="good")
        # elif self.value() == "bad":
        #     return queryset.filter(payload__contains="bad")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "room",
        "experience",
        "rating",
    )

    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
