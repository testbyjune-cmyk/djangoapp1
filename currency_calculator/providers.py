"""
환율 데이터 소스를 플러그인 형태로 교체할 수 있게 하는 provider 계층.

새로운 데이터 소스(예: 외부 환율 API)를 추가하려면 ExchangeRateProvider를
상속한 새 클래스를 만들고 settings.EXCHANGE_RATE_PROVIDER 경로만 바꾸면
된다. 기존 코드(서비스/뷰)는 전혀 수정할 필요가 없다 (개방-폐쇄 원칙).
"""

from abc import ABC, abstractmethod
from decimal import Decimal

from django.conf import settings
from django.utils.module_loading import import_string


class CurrencyNotSupportedError(Exception):
    pass


class ExchangeRateProvider(ABC):
    """환율 조회를 위한 최소 인터페이스 (인터페이스 분리 원칙)."""

    @abstractmethod
    def get_rate(self, currency_code: str) -> Decimal:
        """1 단위의 currency_code를 KRW로 환산한 값을 반환한다."""
        raise NotImplementedError

    @abstractmethod
    def list_currencies(self):
        """선택 가능한 통화 목록을 반환한다."""
        raise NotImplementedError


class DatabaseExchangeRateProvider(ExchangeRateProvider):
    """DB(ExchangeRate 모델)에 저장된 환율을 사용하는 기본 provider."""

    def get_rate(self, currency_code: str) -> Decimal:
        from .models import ExchangeRate

        try:
            return ExchangeRate.objects.get(currency_code=currency_code).rate_to_krw
        except ExchangeRate.DoesNotExist as exc:
            raise CurrencyNotSupportedError(currency_code) from exc

    def list_currencies(self):
        from .models import ExchangeRate

        return list(ExchangeRate.objects.all())


def get_exchange_rate_provider() -> ExchangeRateProvider:
    """settings에 설정된 provider 클래스를 로드한다 (의존관계 역전 원칙)."""

    provider_path = getattr(
        settings,
        "EXCHANGE_RATE_PROVIDER",
        "currency_calculator.providers.DatabaseExchangeRateProvider",
    )
    provider_class = import_string(provider_path)
    return provider_class()
