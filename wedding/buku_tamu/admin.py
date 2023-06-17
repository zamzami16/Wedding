from django.contrib import admin

from .models import BukuTamu


@admin.register(BukuTamu)
class BukuTamuAdmin(admin.ModelAdmin):
    ordering = ["inviter"]
    list_display = ["id", "inviter", "nama", "kehadiran", "ucapan"]
    list_filter = ["inviter", "kehadiran"]
