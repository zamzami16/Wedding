from django.contrib import admin

from .models import BukuTamu


@admin.register(BukuTamu)
class BukuTamuAdmin(admin.ModelAdmin):
    ordering = ["inviter"]
