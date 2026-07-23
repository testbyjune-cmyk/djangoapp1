from django.apps import AppConfig


class CurrencyCalculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "currency_calculator"

    def ready(self):
        from core.navigation import register

        register(
            "환율 계산기",
            "currency_calculator:calculator",
            app_label="currency_calculator",
            order=10,
        )
