from django.contrib import admin

from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("currency_code", "currency_name", "symbol", "rate_to_krw", "updated_at")
    search_fields = ("currency_code", "currency_name")
