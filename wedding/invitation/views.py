from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
    BasicAuthentication,
)
from .models import Profile
from django.contrib.auth import authenticate
from .serializers import UsersSerializer, ProfileSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UsersSerializer


class UserUpdate(generics.UpdateAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(
            {"status": "failed", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserProfile(generics.CreateAPIView):
    pass


class LoginView(APIView):
    permission_classes = ()

    def post(
        self,
        request,
    ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_authenticated:
            return Response(
                {"status": "success", "data": {"token": user.auth_token.key}}
            )
        else:
            return Response(
                {"errors": "username dan password tidak cocok"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CustomAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if user is None or not user.is_authenticated:
            return Response(
                {
                    "status": "failed",
                    "message": "Username dan Password tidak valid.",
                }
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "status": "success",
                "data": {
                    "userid": user.id,
                    "token": token.key,
                },
            },
            status=status.HTTP_200_OK,
        )


class UserProfileView(generics.RetrieveAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Customize the response data
        response_data = {
            "status": "success",
            "message": "Profile retrieved successfully",
            "data": serializer.data,
        }

        return Response(response_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Customize the response data
        response_data = {
            "status": "success",
            "message": "Profile created successfully",
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
