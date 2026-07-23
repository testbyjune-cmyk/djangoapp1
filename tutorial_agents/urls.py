from django.urls import path

from .views import AgentsLessonView

app_name = "tutorial_agents"

urlpatterns = [
    path("", AgentsLessonView.as_view(), name="lesson"),
]
