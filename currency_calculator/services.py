"""환율 계산 비즈니스 로직 (단일 책임 원칙: 계산만 담당, HTTP/DB 접근은 다루지 않음)."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from .providers import ExchangeRateProvider


@dataclass(frozen=True)
class ConversionResult:
    amount: Decimal
    currency_code: str
    rate_to_krw: Decimal
    krw_amount: Decimal
    foreign_amount: Decimal


class CurrencyConverterService:
    """구체적인 provider 구현이 아니라 추상 인터페이스에 의존한다 (DIP)."""

    def __init__(self, provider: ExchangeRateProvider):
        self._provider = provider

    def list_currencies(self):
        return self._provider.list_currencies()

    def convert_to_krw(self, amount: Decimal, currency_code: str) -> ConversionResult:
        rate = self._provider.get_rate(currency_code)
        krw_amount = self._round(amount * rate)
        return ConversionResult(
            amount=amount,
            currency_code=currency_code,
            rate_to_krw=rate,
            krw_amount=krw_amount,
            foreign_amount=amount,
        )

    def convert_from_krw(self, krw_amount: Decimal, currency_code: str) -> ConversionResult:
        rate = self._provider.get_rate(currency_code)
        foreign_amount = self._round(krw_amount / rate)
        return ConversionResult(
            amount=krw_amount,
            currency_code=currency_code,
            rate_to_krw=rate,
            krw_amount=self._round(krw_amount),
            foreign_amount=foreign_amount,
        )

    @staticmethod
    def _round(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
