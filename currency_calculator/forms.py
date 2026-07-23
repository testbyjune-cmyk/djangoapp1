from decimal import Decimal

from django import forms

DIRECTION_CHOICES = [
    ("to_krw", "외화 → 원화(KRW)"),
    ("from_krw", "원화(KRW) → 외화"),
]


class ConversionForm(forms.Form):
    """오류 예방(Nielsen #5)을 위해 드롭다운/숫자 필드로 잘못된 입력을 원천 차단한다."""

    amount = forms.DecimalField(
        label="금액",
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"step": "0.01", "placeholder": "예: 100", "class": "form-control"}
        ),
    )
    currency_code = forms.ChoiceField(
        label="통화", widget=forms.Select(attrs={"class": "form-select"})
    )
    direction = forms.ChoiceField(
        label="변환 방향",
        choices=DIRECTION_CHOICES,
        initial="to_krw",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, currency_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["currency_code"].choices = currency_choices
