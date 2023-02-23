from rest_framework import serializers
from .models import Review

from users.serializers import TinyUserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    # review를 달때는 user한테 user정보를 받지 않음
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
