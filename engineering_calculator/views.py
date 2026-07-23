import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .operations import CalculationError
from .services import EngineeringCalculatorService


class EngineeringCalculatorView(TemplateView):
    template_name = "engineering_calculator/calculator.html"


class CalculateAPIView(View):
    """단항/이항 연산을 계산해 JSON으로 결과 또는 오류 메시지를 반환한다."""

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

        operator_code = payload.get("operator")
        angle_mode = payload.get("angle_mode", "deg")

        try:
            operands = [float(value) for value in payload.get("operands", [])]
        except (TypeError, ValueError):
            return JsonResponse({"error": "숫자만 입력할 수 있습니다."}, status=400)

        service = EngineeringCalculatorService()
        try:
            result = service.evaluate(operator_code, operands, angle_mode=angle_mode)
        except CalculationError as exc:
            return JsonResponse({"error": str(exc)}, status=400)
        except (ValueError, OverflowError):
            return JsonResponse({"error": "계산할 수 없는 값입니다."}, status=400)

        return JsonResponse({"result": result})
