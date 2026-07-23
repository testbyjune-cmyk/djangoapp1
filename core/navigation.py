"""
네비게이션 항목 레지스트리.

각 앱(플러그인)은 자신의 apps.py의 ready()에서 register()를 호출해
스스로를 네비게이션에 등록한다. core나 base.html을 수정하지 않고도
새 앱을 추가/제거할 수 있다 (개방-폐쇄 원칙).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NavItem:
    label: str
    url_name: str
    order: int = 0


_registry: list[NavItem] = []


def register(label: str, url_name: str, order: int = 0) -> None:
    if any(item.url_name == url_name for item in _registry):
        return
    _registry.append(NavItem(label=label, url_name=url_name, order=order))
    _registry.sort(key=lambda item: item.order)


def get_nav_items() -> list[NavItem]:
    return list(_registry)
