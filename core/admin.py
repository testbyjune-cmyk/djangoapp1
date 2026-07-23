from django.contrib import admin

from .models import AppToggle


@admin.register(AppToggle)
class AppToggleAdmin(admin.ModelAdmin):
    list_display = ("display_name", "app_label", "is_enabled")
    list_editable = ("is_enabled",)
