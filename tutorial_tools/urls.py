from django.urls import path

from .views import ToolsLessonView

app_name = "tutorial_tools"

urlpatterns = [
    path("", ToolsLessonView.as_view(), name="lesson"),
]
