from django.urls import path
from .views import (
    register_view,
    LoginView,
    DeleteUserView,
    CreateProfileView,
    UpdateProfileView,
    ListAllProfileView,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "delete-account/", DeleteUserView.as_view(), name="delete_account_view"
    ),
    path(
        "profile/update/",
        UpdateProfileView.as_view(),
        name="update_user_profile",
    ),
    path("profile/", CreateProfileView.as_view(), name="create_user_profile"),
    path("profiles/", ListAllProfileView.as_view(), name="list_profiles"),
]
