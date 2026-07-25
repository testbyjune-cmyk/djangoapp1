from django.urls import path

from .views import (
    CommentCreateView,
    CommentDeleteView,
    HomeView,
    SettingsView,
    ToggleProgressView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("progress/toggle/", ToggleProgressView.as_view(), name="toggle_progress"),
    path("comments/<str:page_key>/create/", CommentCreateView.as_view(), name="comment_create"),
    path(
        "comments/<str:page_key>/<str:entry_id>/delete/",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
