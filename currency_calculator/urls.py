from django.urls import path

from .views import CurrencyCalculatorView

app_name = "currency_calculator"

urlpatterns = [
    path("", CurrencyCalculatorView.as_view(), name="calculator"),
]
