from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        """Update password"""
        instance.username = validated_data.get("username", instance.username)
        password = validated_data.get("password", instance.password)
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(password)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("__all__",)

    # def create(self, validated_data, user):
    #     profile = Profile.objects.create(
    #         user=user,
    #         nama_pengantin_lk=validated_data["nama_pengantin_lk"],
    #         nama_pengantin_pr=validated_data["nama_pengantin_pr"],
    #         nama_panggilan_lk=validated_data["nama_panggilan_lk"],
    #         nama_panggilan_pr=validated_data["nama_panggilan_pr"],
    #         nama_wali_lk_ayah=validated_data["nama_wali_lk_ayah"],
    #         nama_wali_lk_ibu=validated_data["nama_wali_lk_ibu"],
    #         nama_wali_pr_ayah=validated_data["nama_wali_pr_ayah"],
    #         nama_wali_pr_ibu=validated_data["nama_wali_pr_ibu"],
    #     )
    #     return profile
