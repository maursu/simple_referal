from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework import serializers

from . import models
from . import tasks


User = get_user_model()


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "invite_code",
            "login_code",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "invite_code",
            "login_code",
            "created_at",
            "updated_at",
        ]

    def validate_phone_number(self, phone_number):
        if not phone_number.startswith("+"):
            raise serializers.ValidationError(
                "Phone number must start with country code"
            )
        if not len(phone_number) >= 7:
            raise serializers.ValidationError("Invalid phone number")
        return phone_number

    def send_login_code(self, user):
        phone_number = user.phone_number
        user.set_login_code()
        tasks.send_login_code.delay()
        tasks.delete_login_code.apply_async((phone_number,), countdown=1 * 30)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.send_login_code(user)
        models.UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["login_code"]
        extra_kwargs = {"login_code": {"required": True, "write_only": True}}

    def validate_login_code(self, login_code):
        if not login_code:
            raise serializers.ValidationError("This field can not be blank")
        return login_code

    def validate(self, attrs):
        request = self.context["request"]
        login_code = attrs["login_code"]
        user = User.objects.filter(login_code=login_code)
        if not user:
            raise serializers.ValidationError("Wrong login code")
        attrs["user"] = user[0]
        login(request=request, user=user[0])
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = [
            "id",
            "refered_by",
        ]
        read_only_fields = ["id", "user"]

    def validate_refered_by(self, refered_by):
        users = User.objects.all()
        codes = list(map(lambda user: user.invite_code, users))
        if not refered_by in codes:
            return serializers.ValidationError("Invalid invite code")
        return refered_by

    def update(self, instance, validated_data):
        if instance.refered_by:
            return instance
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = UserSerializer(instance=instance.user).data
        invite_code = instance.user.invite_code
        queryset = self.context["view"].queryset.filter(refered_by=invite_code)
        phone_numbers = list(map(lambda profile: profile.user.phone_number, queryset))

        representation["phone_number"] = user_data["phone_number"]
        representation["invite_code"] = user_data["invite_code"]
        representation["created_at"] = user_data["created_at"]
        representation["invited_users"] = phone_numbers
        return representation
