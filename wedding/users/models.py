from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
