from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room

from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

from reviews.serializers import ReviewSerializer

from medias.serializers import PhotoSerializer

from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, obj):
        return obj.rating()

    def get_is_owner(self, obj):
        return obj.owner.pk == self.context["request"].user.pk


class RoomDetailSerializer(ModelSerializer):
    # relationships
    # 원하는 필드에 원하는 시리얼라이저 적용 가능
    # owner는 request.data에서 받으면 안됨! request object에서 받아야 함
    owner = TinyUserSerializer(read_only=True)
    # read_only=True 로 설정하면 serializer는 post할 때 해당 정보를 요구하지 않음
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    # serializer에서 method field를 사용하여 원하는 정보를 보여줄 수 있음
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        # for relationships, 근데 이건 다 가져옴
        # depth = 1

    # serializer에서 method field를 사용하려면 get_메소드명 으로 정의해야 함
    def get_rating(self, obj):
        # return "it working!! "
        print(self.context.get("request").user)
        test = obj.reviews.all()
        print(test.count())
        return obj.rating()

    # practice for context
    def get_is_owner(self, obj):
        return obj.owner == self.context.get("request").user

    def get_is_liked(self, obj):
        request = self.context.get("request")
        return Wishlist.objects.filter(
            user=request.user,
            rooms__id=obj.pk,
        ).exists()

    # view에서 serializer.save가 불리면 create method가 호출 됨

    # def create(self, validated_data):
    # return Room.objects.create(**validated_data)

    ### SerializerMethodField로 만드는 dynamic field는
    ### 해당 객체를 바라보는 사람에 따라 다른 값을 보여줄 수 있어서 매우 유용함
    ### 예를 들어, instagram에서는 내가 좋아요를 누른 게시물에는 좋아요를 누른 사람들의 목록이 보이지 않음
    ### 이런 경우에는 serializer에서 method field를 사용하여 해당 게시물을 보는 사람이 좋아요를 눌렀는지 여부를
    ### dynamic field로 보여줄 수 있음

    ### reverse accessor
    ### reviews = ReviewSerializer(many=True, read_only=True)
    ### 모든 리뷰를 가져옴, 좋은 방법이 아님
    ### pagination을 적용하면 좋음
