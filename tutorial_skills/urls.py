from django.urls import path

from .views import SkillsLessonView

app_name = "tutorial_skills"

urlpatterns = [
    path("", SkillsLessonView.as_view(), name="lesson"),
]
