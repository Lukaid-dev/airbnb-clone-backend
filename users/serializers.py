from rest_framework.serializers import ModelSerializer

from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    # ModelSerializer는 기본적으로 Uniqueness를 검사함
    # 근데 어떤 필드를 검사하는건지?
    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "first_name",
            "last_name",
            "user_permissions",
        )
