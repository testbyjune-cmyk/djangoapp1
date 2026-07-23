from django.urls import path

from .views import WorktreeLessonView

app_name = "tutorial_worktree"

urlpatterns = [
    path("", WorktreeLessonView.as_view(), name="lesson"),
]
