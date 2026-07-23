"""공학 계산기 계산 로직 (단일 책임 원칙: HTTP/직렬화는 다루지 않고 계산만 담당)."""

from .operations import CalculationError, get_operation


class EngineeringCalculatorService:
    def evaluate(self, operator_code: str, operands: list[float], angle_mode: str = "deg") -> float:
        operation = get_operation(operator_code)

        if len(operands) != operation.arity:
            raise CalculationError(
                f"'{operation.label}' 연산에는 값이 {operation.arity}개 필요합니다."
            )

        if operation.needs_angle_mode:
            return operation.compute(*operands, angle_mode=angle_mode)
        return operation.compute(*operands)
