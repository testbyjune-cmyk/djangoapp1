from django.urls import path

from .views import CalculateAPIView, EngineeringCalculatorView

app_name = "engineering_calculator"

urlpatterns = [
    path("", EngineeringCalculatorView.as_view(), name="calculator"),
    path("calculate/", CalculateAPIView.as_view(), name="calculate_api"),
]
