from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import empty
from .models import Invitation


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class InvitationSerializer(serializers.ModelSerializer):
    inviter = UsersSerializer()

    class Meta:
        model = Invitation
        fields = "__all__"

    def create(self, validated_data):
        invitation = Invitation(
            inviter=User.objects.get(username=validated_data["inviter"]),
            name=validated_data["name"],
            alamat=validated_data["alamat"],
        )
        invitation.save()
        return invitation


class InvitationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"


class InvitationCreateSerializer(serializers.ModelSerializer):
    inviter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Invitation
        fields = [
            "id",
            "inviter",
            "name",
            "alamat",
        ]

    def create(self, validated_data):
        instance = Invitation(
            inviter=validated_data["inviter"],
            name=validated_data["name"],
            alamat=validated_data["name"],
        )
        instance.save()
        return instance
