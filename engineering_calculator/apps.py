from django.apps import AppConfig


class EngineeringCalculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "engineering_calculator"

    def ready(self):
        from core.navigation import register

        register(
            "공학 계산기",
            "engineering_calculator:calculator",
            app_label="engineering_calculator",
            order=5,
        )
