from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            return serializers.ValidationError(
                {"status": "error", "message": "password did not match"}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("username", "password")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "id",
            "nama_pengantin_lk",
            "nama_pengantin_pr",
            "nama_panggilan_lk",
            "nama_panggilan_pr",
            "nama_wali_lk_ayah",
            "nama_wali_lk_ibu",
            "nama_wali_pr_ayah",
            "nama_wali_pr_ibu",
            "user",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = [
            "nama_pengantin_lk",
            "nama_pengantin_pr",
            "nama_panggilan_lk",
            "nama_panggilan_pr",
            "nama_wali_lk_ayah",
            "nama_wali_lk_ibu",
            "nama_wali_pr_ayah",
            "nama_wali_pr_ibu",
            "user",
        ]

    def update(self, instance, validated_data):
        instance.nama_pengantin_lk = validated_data.get(
            "nama_pengantin_lk", instance.nama_pengantin_lk
        )
        instance.nama_pengantin_pr = validated_data.get(
            "nama_pengantin_pr", instance.nama_pengantin_pr
        )
        instance.nama_panggilan_lk = validated_data.get(
            "nama_panggilan_lk", instance.nama_panggilan_lk
        )
        instance.nama_panggilan_pr = validated_data.get(
            "nama_panggilan_pr", instance.nama_panggilan_pr
        )
        instance.nama_wali_lk_ayah = validated_data.get(
            "nama_wali_lk_ayah", instance.nama_wali_lk_ayah
        )
        instance.nama_wali_pr_ayah = validated_data.get(
            "nama_wali_pr_ayah", instance.nama_wali_pr_ayah
        )
        instance.nama_wali_lk_ibu = validated_data.get(
            "nama_wali_lk_ibu", instance.nama_wali_lk_ibu
        )
        instance.nama_wali_pr_ibu = validated_data.get(
            "nama_wali_pr_ibu", instance.nama_wali_pr_ibu
        )
        instance.save()
        return instance
