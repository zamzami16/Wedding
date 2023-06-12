from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

pilihan_hadir = []


class BukuTamu(models.Model):
    """Model untuk buku tamu"""

    hadir = "HA"
    tidak_hadir = "TH"
    belum_tahu = "BT"
    insya_allah = "IA"
    kehadiran_choices = [
        (hadir, "Hadir"),
        (tidak_hadir, "Tidak Hadir"),
        (belum_tahu, "Belum Tahu"),
        (insya_allah, "Insya Allah Hadir"),
    ]

    inviter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user"
    )
    nama = models.CharField(
        _("nama tamu"), max_length=200, blank=False, default="anonim"
    )
    kehadiran = models.CharField(
        max_length=2, choices=kehadiran_choices, default=hadir
    )
    ucapan = models.TextField(verbose_name="ucapan tamu kepada user")

    class Meta:
        ordering = ["inviter"]

    def get_all_ucapan(self):
        """Get all ucapan dan nama dari tamu"""
        pass
