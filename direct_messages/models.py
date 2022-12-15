from django.db import models
from common.models import CommonModel


class ChanttingRoom(CommonModel):
    """
    - Room Model Definition
    - 모델의 이름이 같다는건 문제가 되지 않음
    - 근데 두 모델 전부 하나의 같은 모델을 참조하고 있으면 문제가 발생함
    - 이때 related_name을 사용하면 문제를 해결할 수 있음
    """

    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self):
        return f"ChanttingRoom {self.id}"


class Message(CommonModel):
    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "direct_messages.ChanttingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"
