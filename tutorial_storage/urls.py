from django.urls import path

from .views import GuestbookCreateView, GuestbookDeleteView, StorageLessonView

app_name = "tutorial_storage"

urlpatterns = [
    path("", StorageLessonView.as_view(), name="lesson"),
    path("guestbook/create/", GuestbookCreateView.as_view(), name="guestbook_create"),
    path("guestbook/<int:pk>/delete/", GuestbookDeleteView.as_view(), name="guestbook_delete"),
]
