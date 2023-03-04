from django.db import models
from django.contrib.auth.models import AbstractUser

# 내가 원하는 유저 모델을 만들 수 있음, 이름을 꼭 User로 해야하는 것은 아님
# config/settings.py에 AUTH_USER_MODEL = 'users.User'를 추가해야함
# 중간에 있는 유저 데이터를 옮길 수 없으므로 프로젝트의 시작에서 만들어 줘야 함


class User(AbstractUser):
    class Meta:
        default_related_name = "users"

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")  # (value for db, label for admin)
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("ko", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        KRW = ("KRW", "Korean Won")
        USD = ("USD", "US Dollar")

    # 기존 모델에 있는 필드를 사용하지 않고 새로운 필드를 추가할 수 있음
    first_name = models.CharField(
        max_length=150,
        blank=True,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        editable=False,
    )
    avatar = models.URLField(
        blank=True,
    )
    name = models.CharField(
        max_length=150,
        blank=False,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
    )
