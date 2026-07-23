from django.views.generic import FormView

from .forms import ConversionForm
from .providers import CurrencyNotSupportedError, get_exchange_rate_provider
from .services import CurrencyConverterService


class CurrencyCalculatorView(FormView):
    template_name = "currency_calculator/calculator.html"
    form_class = ConversionForm

    def get_service(self) -> CurrencyConverterService:
        return CurrencyConverterService(get_exchange_rate_provider())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        service = self.get_service()
        kwargs["currency_choices"] = [
            (c.currency_code, f"{c.currency_code} - {c.currency_name}")
            for c in service.list_currencies()
        ]
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["currencies"] = self.get_service().list_currencies()
        return context

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(form=form)

        if form.is_valid():
            service = self.get_service()
            amount = form.cleaned_data["amount"]
            currency_code = form.cleaned_data["currency_code"]
            direction = form.cleaned_data["direction"]

            try:
                if direction == "to_krw":
                    result = service.convert_to_krw(amount, currency_code)
                else:
                    result = service.convert_from_krw(amount, currency_code)
                context["result"] = result
            except CurrencyNotSupportedError:
                form.add_error("currency_code", "지원하지 않는 통화입니다.")

        return self.render_to_response(context)
