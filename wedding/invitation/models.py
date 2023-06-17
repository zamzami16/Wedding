from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Invitation(models.Model):
    id = models.BigAutoField(_("Invitation id"), primary_key=True)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(_("nama yang diundang"), max_length=200, null=False)
    alamat = models.CharField(
        _("alamat yang di undang"), max_length=500, null=True
    )

    class Meta:
        ordering = ("inviter",)

    def __str__(self):
        return self.name
