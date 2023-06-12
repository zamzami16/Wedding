from rest_framework import serializers
from django.contrib.auth.models import User
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
