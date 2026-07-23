from django.urls import path

from .views import HomeView, SettingsView, ToggleProgressView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("progress/toggle/", ToggleProgressView.as_view(), name="toggle_progress"),
]
