from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Booking


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class CreateBookingSerializer(ModelSerializer):
    # model에선 guest만 required이기 떄문에 client에서 guest만 보내도 valid하다고 나옴
    # 근데 상황에 따라 valid조건이 달라지기 때문에 serializer에서 validate를 통해 조건을 추가해줘야함

    # This field is required.

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # add additional validation to return false if date is in the past
    # def validate_<field_name>(self, data):
    # value is the value of the field
    # def validate_check_in(self, value):
    #     now = timezone.now().astimezone()
    #     if value < now:
    #         raise serializers.ValidationError("Can't book in the past")
    #     return value

    # def validate_check_out(self, value):
    #     now = timezone.now().astimezone()
    #     if value < now:
    #         raise serializers.ValidationError("Can't book in the past")
    #     return value

    # 그냥 validate를 쓰면 모든 field에 대해 validate를 할 수 있음
    def validate(self, data):
        now = timezone.now().astimezone().date()
        if data.get("check_in") and data.get("check_out"):
            if data.get("check_in") < now:
                raise serializers.ValidationError("Can't book in the past")

            if data.get("check_out") < now:
                raise serializers.ValidationError("Can't book in the past")

            if data.get("check_in") >= data.get("check_out"):
                raise serializers.ValidationError("Check out must be after check in")

            # do not overlap other bookings
            if Booking.objects.filter(
                room=self.context["room"],
                check_in__lte=data.get("check_out"),
                check_out__gte=data.get("check_in"),
            ).exists():
                raise serializers.ValidationError("Room already booked at this time")

        return data
