from user.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers

USERNAME = "username"
PASSWORD = "password"
EMAIL = "email"
ID = "id"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"

PASSWORD_2 = "password2"
USER_FIELDS = [USERNAME, PASSWORD, EMAIL, ID]
WRITE_ONLY_PASSWORD = {PASSWORD: {"write_only": True}}
PASSWORD_INPUT_TYPE = {"input_type": PASSWORD}

USER = get_user_model()


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, style=PASSWORD_INPUT_TYPE
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = USER_FIELDS
        extra_kwargs = WRITE_ONLY_PASSWORD


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = [*USER_FIELDS, FIRST_NAME, LAST_NAME, PASSWORD_2]
        extra_kwargs = WRITE_ONLY_PASSWORD

    def save(self, **kwargs):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        user = get_user_model()(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        user.set_password(password)
        user.save()
        return user
