"""
공학용 계산기의 연산 플러그인 계층.

새 연산을 추가하려면 Operation을 상속한 클래스를 만들어 @register("code")로
등록하기만 하면 된다. 서비스/뷰 코드는 전혀 수정할 필요가 없다 (개방-폐쇄 원칙).
모든 연산은 동일한 compute(*operands) 계약을 따르므로 서로 치환 가능하다 (LSP).
"""

import math
from abc import ABC, abstractmethod


class CalculationError(Exception):
    pass


class Operation(ABC):
    arity: int
    label: str
    needs_angle_mode: bool = False

    @abstractmethod
    def compute(self, *operands):
        raise NotImplementedError


_registry: dict[str, Operation] = {}


def register(code: str):
    def decorator(cls):
        _registry[code] = cls()
        return cls

    return decorator


def get_operation(code: str) -> Operation:
    try:
        return _registry[code]
    except KeyError as exc:
        raise CalculationError(f"지원하지 않는 연산입니다: {code}") from exc


@register("add")
class Add(Operation):
    arity = 2
    label = "+"

    def compute(self, a, b):
        return a + b


@register("subtract")
class Subtract(Operation):
    arity = 2
    label = "−"

    def compute(self, a, b):
        return a - b


@register("multiply")
class Multiply(Operation):
    arity = 2
    label = "×"

    def compute(self, a, b):
        return a * b


@register("divide")
class Divide(Operation):
    arity = 2
    label = "÷"

    def compute(self, a, b):
        if b == 0:
            raise CalculationError("0으로 나눌 수 없습니다.")
        return a / b


@register("power")
class Power(Operation):
    arity = 2
    label = "xʸ"

    def compute(self, a, b):
        try:
            result = a**b
        except OverflowError as exc:
            raise CalculationError("계산 결과가 너무 큽니다.") from exc
        if isinstance(result, complex):
            raise CalculationError("실수 범위를 벗어난 결과입니다.")
        return result


@register("sqrt")
class Sqrt(Operation):
    arity = 1
    label = "√x"

    def compute(self, a):
        if a < 0:
            raise CalculationError("음수의 제곱근은 계산할 수 없습니다.")
        return math.sqrt(a)


@register("square")
class Square(Operation):
    arity = 1
    label = "x²"

    def compute(self, a):
        return a**2


@register("cube")
class Cube(Operation):
    arity = 1
    label = "x³"

    def compute(self, a):
        return a**3


@register("reciprocal")
class Reciprocal(Operation):
    arity = 1
    label = "1/x"

    def compute(self, a):
        if a == 0:
            raise CalculationError("0의 역수는 계산할 수 없습니다.")
        return 1 / a


@register("percent")
class Percent(Operation):
    arity = 1
    label = "%"

    def compute(self, a):
        return a / 100


@register("factorial")
class Factorial(Operation):
    arity = 1
    label = "x!"

    def compute(self, a):
        if a < 0 or a != int(a):
            raise CalculationError("팩토리얼은 0 이상의 정수에만 사용할 수 있습니다.")
        n = int(a)
        if n > 170:
            raise CalculationError("입력값이 너무 큽니다 (170 이하만 지원).")
        return float(math.factorial(n))


@register("log10")
class Log10(Operation):
    arity = 1
    label = "log"

    def compute(self, a):
        if a <= 0:
            raise CalculationError("0 이하의 수는 로그를 계산할 수 없습니다.")
        return math.log10(a)


@register("ln")
class Ln(Operation):
    arity = 1
    label = "ln"

    def compute(self, a):
        if a <= 0:
            raise CalculationError("0 이하의 수는 로그를 계산할 수 없습니다.")
        return math.log(a)


@register("exp")
class Exp(Operation):
    arity = 1
    label = "eˣ"

    def compute(self, a):
        try:
            return math.exp(a)
        except OverflowError as exc:
            raise CalculationError("계산 결과가 너무 큽니다.") from exc


@register("sin")
class Sin(Operation):
    arity = 1
    label = "sin"
    needs_angle_mode = True

    def compute(self, a, angle_mode="deg"):
        rad = math.radians(a) if angle_mode == "deg" else a
        return math.sin(rad)


@register("cos")
class Cos(Operation):
    arity = 1
    label = "cos"
    needs_angle_mode = True

    def compute(self, a, angle_mode="deg"):
        rad = math.radians(a) if angle_mode == "deg" else a
        return math.cos(rad)


@register("tan")
class Tan(Operation):
    arity = 1
    label = "tan"
    needs_angle_mode = True

    def compute(self, a, angle_mode="deg"):
        rad = math.radians(a) if angle_mode == "deg" else a
        if abs(math.cos(rad)) < 1e-12:
            raise CalculationError("정의되지 않은 값입니다 (tan 90°).")
        return math.tan(rad)


@register("asin")
class Asin(Operation):
    arity = 1
    label = "sin⁻¹"
    needs_angle_mode = True

    def compute(self, a, angle_mode="deg"):
        if not -1 <= a <= 1:
            raise CalculationError("정의역을 벗어났습니다 (-1 ~ 1).")
        result = math.asin(a)
        return math.degrees(result) if angle_mode == "deg" else result


@register("acos")
class Acos(Operation):
    arity = 1
    label = "cos⁻¹"
    needs_angle_mode = True

    def compute(self, a, angle_mode="deg"):
        if not -1 <= a <= 1:
            raise CalculationError("정의역을 벗어났습니다 (-1 ~ 1).")
        result = math.acos(a)
        return math.degrees(result) if angle_mode == "deg" else result


@register("atan")
class Atan(Operation):
    arity = 1
    label = "tan⁻¹"
    needs_angle_mode = True

    def compute(self, a, angle_mode="deg"):
        result = math.atan(a)
        return math.degrees(result) if angle_mode == "deg" else result
