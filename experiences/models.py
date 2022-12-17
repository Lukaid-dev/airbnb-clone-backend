from django.db import models

from common.models import CommonModel


class Experience(CommonModel):
    class Meta:
        default_related_name = "experiences"

    """Experience Model Definition"""

    name = models.CharField(
        max_length=250,
    )
    description = models.TextField()
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )
    # 얘가 들고 있는 카테고리가 사라지면 얘를 없애지 않고 그냥 이 필드만 null로 만듬
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    class Meta:
        default_related_name = "perks"

    """What is included in the experience"""

    name = models.CharField(
        max_length=100,
    )
    detail = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    description = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
