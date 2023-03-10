from django.db import models

from common.models import CommonModel


class Wishlist(CommonModel):
    class Meta:
        default_related_name = "wishlists"

    """wishlist Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    # why many to many?
    rooms = models.ManyToManyField(
        "rooms.Room",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
    )

    def __str__(self):
        return self.name
