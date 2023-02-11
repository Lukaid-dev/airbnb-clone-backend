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

    # relationships
    # 원하는 필드에 원하는 시리얼라이저 적용 가능
    # owner는 request.data에서 받으면 안됨! request object에서 받아야 함
    owner = TinyUserSerializer(read_only=True)
    # read_only=True 로 설정하면 serializer는 post할 때 해당 정보를 요구하지 않음
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        # for relationships, 근데 이건 다 가져옴
        # depth = 1

    # view에서 serializer.save가 불리면 create method가 호출 됨

    # def create(self, validated_data):
        # return Room.objects.create(**validated_data)