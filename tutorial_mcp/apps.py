from django.apps import AppConfig


class TutorialMcpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_mcp"

    def ready(self):
        from core.navigation import register

        register(
            "MCP",
            "tutorial_mcp:lesson",
            app_label="tutorial_mcp",
            order=30,
            icon="🔌",
        )
