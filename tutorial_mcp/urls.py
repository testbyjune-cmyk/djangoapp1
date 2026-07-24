from django.urls import path

from .views import McpLessonView

app_name = "tutorial_mcp"

urlpatterns = [
    path("", McpLessonView.as_view(), name="lesson"),
]
