from django.apps import AppConfig


class TutorialAgentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_agents"

    def ready(self):
        from core.navigation import register

        register(
            "에이전트 & 서브에이전트",
            "tutorial_agents:lesson",
            app_label="tutorial_agents",
            order=10,
        )
