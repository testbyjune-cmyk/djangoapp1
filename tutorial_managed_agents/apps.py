from django.apps import AppConfig


class TutorialManagedAgentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_managed_agents"

    def ready(self):
        from core.navigation import register

        register(
            "Managed Agent",
            "tutorial_managed_agents:lesson",
            app_label="tutorial_managed_agents",
            order=35,
            icon="☁️",
        )
