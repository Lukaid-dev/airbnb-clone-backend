from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    class Meta:
        default_related_name = "photos"

    """Photo Model Definition"""

    # file = models.ImageField()
    file = models.URLField()  # for security
    description = models.TextField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.room:
            return f"Photo for {self.room.name}"
        elif self.experience:
            return f"Photo for {self.experience.name}"
        else:
            return ""


class Video(CommonModel):
    class Meta:
        default_related_name = "videos"

    """Video Model Definition"""

    # file = models.FileField()
    file = models.URLField()  # for security
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Video for {self.experience.name}"
