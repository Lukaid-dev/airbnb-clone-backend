from django.db import models

from common.models import CommonModel


class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE = ("entire", "Entire Place")
        PRIVATE = ("private", "Private Room")
        SHARED = ("shared", "Shared Room")

    name = models.CharField(
        max_length=180,
    )
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friednly = models.BooleanField(
        default=True,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
        blank=True,
    )
    categore = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    # def total_amenities(self):
    #     print("test")
    #     return self.amenities.count() * 2


class Amenity(CommonModel):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,  # db side
        blank=True,  # django side
    )

    def __str__(self):
        return self.name
