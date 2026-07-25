from django.urls import path

from .views import StorageLessonView

app_name = "tutorial_storage"

urlpatterns = [
    path("", StorageLessonView.as_view(), name="lesson"),
]
