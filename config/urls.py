from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("currency/", include("currency_calculator.urls")),
    path("engineering/", include("engineering_calculator.urls")),
]
