from django.urls import path

from .views import ManagedAgentsLessonView

app_name = "tutorial_managed_agents"

urlpatterns = [
    path("", ManagedAgentsLessonView.as_view(), name="lesson"),
]
