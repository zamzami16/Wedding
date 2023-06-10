from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from .managers import UsersManager



class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    nama_pengantin_lk = models.CharField(max_length=200, null=False)
    nama_pengantin_pr = models.CharField(max_length=200, null=False)
    nama_panggilan_lk = models.CharField(max_length=200)
    nama_panggilan_pr = models.CharField(max_length=200)
    nama_wali_lk_ayah = models.CharField(max_length=200)
    nama_wali_lk_ibu = models.CharField(max_length=200)
    nama_wali_pr_ayah = models.CharField(
        max_length=200,
    )
    nama_wali_pr_ibu = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class Wedding(models.Model):
    id = models.BigAutoField(_("wedding id"), primary_key=True)
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="wedding"
    )
    hari_pelaksanaan = models.DateField(null=False)
    jam_akad = models.TimeField(null=False)
    jam_resepsi = models.TimeField(null=False)
    tempat = models.CharField(max_length=500)
    url_gmaps = models.URLField("url_alamat", max_length=200)
