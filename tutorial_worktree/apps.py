from django.apps import AppConfig


class TutorialWorktreeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_worktree"

    def ready(self):
        from core.navigation import register

        register(
            "워크트리 & 병렬 작업",
            "tutorial_worktree:lesson",
            app_label="tutorial_worktree",
            order=20,
            icon="🌳",
        )
