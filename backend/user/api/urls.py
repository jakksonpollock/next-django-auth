from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CustomTokenRefreshView,
    UserView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


urlpatterns = [
    path(r"register/", RegisterView.as_view(), name="register"),
    path(r"login/", LoginView.as_view(), name="login"),
    path(r"logout/", LogoutView.as_view(), name="logout"),
    path(r"token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path(r"user/", UserView.as_view(), name="user"),
]
