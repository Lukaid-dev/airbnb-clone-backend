from django.db import models

from common.models import CommonModel


class Booking(CommonModel):
    class Meta:
        default_related_name = "bookings"

    """Booking Model Definition"""

    # 아무리 생각해도 이렇게 app을 쪼개는게 굳이 필요한가 싶다.
    # 연습용이라면 이해가 됨

    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    kind = models.CharField(
        max_length=20,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # experience인 경우 null
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    # room인 경우 null
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return f"{self.kind.title()} for {self.user}"
