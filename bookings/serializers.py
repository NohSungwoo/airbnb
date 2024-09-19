from django.utils import timezone
from rest_framework import serializers

from experiences.serializers import TinyExperienceSerializer
from .models import Booking
from django.utils import timezone


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "kind",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class ExperienceBookingSerializer(serializers.ModelSerializer):

    experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "pk",
            "kind",
            "experience",
            "experience_time",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())

        if value < now:
            raise serializers.ValidationError("experience_time can not past")

        return value



class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # validate_column으로 해당 컬럼의 값을 검증할 수 있다.
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("can't in the past")

        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("can't in the past")

        return value

    # validate만 사용하면 전체 데이터를 검증한다.
    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out"
            )

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken"
            )

        return data
