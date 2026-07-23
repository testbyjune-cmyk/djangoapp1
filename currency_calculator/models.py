from django.db import models


class ExchangeRate(models.Model):
    """1 단위의 외화(currency_code)를 원화(KRW)로 환산한 환율."""

    currency_code = models.CharField(max_length=3, unique=True)
    currency_name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5, blank=True)
    rate_to_krw = models.DecimalField(max_digits=12, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["currency_code"]

    def __str__(self):
        return f"{self.currency_code} = {self.rate_to_krw} KRW"
