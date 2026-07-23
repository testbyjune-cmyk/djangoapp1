from django.apps import AppConfig


class TutorialSkillsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial_skills"

    def ready(self):
        from core.navigation import register

        register(
            "스킬 & 커스터마이징",
            "tutorial_skills:lesson",
            app_label="tutorial_skills",
            order=25,
        )
