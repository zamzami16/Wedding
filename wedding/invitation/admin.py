from django.contrib import admin
from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    ordering = ["inviter", "name"]
    list_filter = ["inviter"]
    list_display = ["id", "inviter", "name", "alamat"]
