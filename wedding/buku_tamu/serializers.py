from rest_framework import serializers
from django.contrib.auth.models import User

from .models import BukuTamu


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class BukuTamuSerializer(serializers.ModelSerializer):
    inviter = UserSerializer()

    class Meta:
        model = BukuTamu
        fields = [
            "id",
            "inviter",
            "nama",
            "kehadiran",
            "ucapan",
        ]


class BukuTamuCreateSerializer(serializers.ModelSerializer):
    inviter_username = serializers.CharField(write_only=True)
    inviter = UserSerializer(required=False)

    class Meta:
        model = BukuTamu
        fields = [
            "id",
            "inviter_username",
            "inviter",
            "nama",
            "kehadiran",
            "ucapan",
        ]

    def create(self, validated_data):
        inviter_username = validated_data.pop("inviter_username")
        inviter = User.objects.get(username=inviter_username)
        validated_data["inviter"] = inviter
        return super().create(validated_data)
