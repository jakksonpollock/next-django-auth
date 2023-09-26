from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import AuthSerializer, RegistrationSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from .utils import get_tokens_for_user
from rest_framework_simplejwt.views import TokenRefreshView

USERNAME = "username"
PASSWORD = "password"

# Create your views here.


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")

            if access_token:
                # Decode the new access token to get its expiration time
                expiration_time = self.get_access_token_expiration(access_token)

                if expiration_time:
                    response.data["exp_time_seconds"] = expiration_time

        return response

    @staticmethod
    def get_access_token_expiration(access_token):
        from rest_framework_simplejwt.tokens import AccessToken

        try:
            decoded_token = AccessToken(access_token)
            expiration_timestamp = int(decoded_token["exp"])
            return expiration_timestamp
        except Exception as e:
            return None


class RegisterView(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Registration Success", **serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=request.data.get(USERNAME),
            password=request.data.get(PASSWORD),
        )
        if user is not None:
            login(request, user)
            token_data = get_tokens_for_user(request.user)
            user = UserSerializer(user)
            return Response(
                {"message": "Login Success", "user": user.data, **token_data},
                status=status.HTTP_200_OK,
            )
        raise exceptions.NotAuthenticated("No such user exists")


class LogoutView(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        logout(request)
        return Response(
            {"message": "Successfully Logged out"}, status=status.HTTP_200_OK
        )


class UserView(APIView):
    @staticmethod
    def get(request):
        user = UserSerializer(request.user)
        return Response(
            {"message": "User Details", "user": user.data}, status=status.HTTP_200_OK
        )
