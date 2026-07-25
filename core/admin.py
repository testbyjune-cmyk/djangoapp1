from django.contrib import admin

from .models import AppToggle, Comment


@admin.register(AppToggle)
class AppToggleAdmin(admin.ModelAdmin):
    list_display = ("display_name", "app_label", "is_enabled")
    list_editable = ("is_enabled",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("page_key", "text", "created_at")
    list_filter = ("page_key",)
