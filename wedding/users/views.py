from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from .models import Profile


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == "GET":
        serializer = RegisterSerializer()
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "silakan login.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            print(user)
        except ValidationError as e:
            return Response(
                {
                    "status": "failed",
                    "message": e.detail,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception:
            return Response(
                {
                    "status": "failed",
                    "message": "Username and Password not valid.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "status": "success",
                "data": {
                    "userid": user.id,
                    "username": user.username,
                    "token": token.key,
                },
            },
            status=status.HTTP_200_OK,
        )


class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)

        return Response(
            {"status": "success", "message": f"user {user} was deleted."},
            status=status.HTTP_200_OK,
        )

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            return Response(
                {"status": "failed", "message": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().handle_exception(exc)


# Post method
class CreateProfileView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except Exception as e:
            return Response(
                {
                    "status": "failed",
                    "message": "Profile creation failed",
                    "detail": str(e),
                },
                status=status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(
            {
                "status": "success",
                "message": "Profile creation successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save()

    def get_object(self):
        user_id = self.request.data.get("user")
        return get_object_or_404(Profile, user_id=user_id)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=self.request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_update(serializer)
            return Response(
                {
                    "status": "success",
                    "message": "Profile updated.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "status": "failed",
                    "message": "Profile update failed.",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListAllProfileView(generics.ListAPIView):
    """Get List of all user profiles"""

    queryset = Profile.objects.all()
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "failed", "message": "No user profiles found."},
                status=status.HTTP_404_NOT_FOUND,
            )
