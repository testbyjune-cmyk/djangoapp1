from django.apps import AppConfig


class TutorialToolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_tools"

    def ready(self):
        from core.navigation import register

        register(
            "핵심 도구",
            "tutorial_tools:lesson",
            app_label="tutorial_tools",
            order=15,
        )
