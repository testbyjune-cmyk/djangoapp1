from django.apps import AppConfig


class TutorialStorageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_storage"

    def ready(self):
        from core.navigation import register

        register(
            "Vercel 스토리지",
            "tutorial_storage:lesson",
            app_label="tutorial_storage",
            order=40,
            icon="🪣",
        )
