from django.urls import path
from rest_framework import routers
from .views import (
    UserCreate,
    LoginView,
    UserUpdate,
    CustomAuthTokenView,
    UserProfileView,
)


urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path("users/<int:pk>/", UserUpdate.as_view(), name="user_update"),
    path("login/", CustomAuthTokenView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
