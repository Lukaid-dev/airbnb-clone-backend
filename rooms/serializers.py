from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room

from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )


class RoomDetailSerializer(ModelSerializer):

    # 원하는 필드에 원하는 시리얼라이저 적용 가능
    # owner는 request.data에서 받으면 안됨!
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
        # for relationships, 근데 이건 다 가져옴
        # depth = 1
