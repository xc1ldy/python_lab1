from toolkit.constants import Token, TokenType
from toolkit.errors import (
    DivisionByZeroError,
    InvalidCharacterError,
    MissingOperandError,
    ShortStackError,
)
from toolkit.tokenize import tokenize
from toolkit.validation import _resolve_unary, _to_rpn


def _evaluate_rpn(rpn_tokens: list[Token]) -> int | float:
    stack: list[int | float] = []

    for token in rpn_tokens:
        if token.type is TokenType.NUMBER:
            value = float(token.value) if "." in token.value else int(token.value)
            stack.append(value)
            continue

        if token.type in (TokenType.NEG, TokenType.POS):
            if not stack:
                raise MissingOperandError("Потерян оператор")
            operand = stack.pop()
            result = -operand if token.type is TokenType.NEG else operand
            stack.append(result)
            continue

        if len(stack) < 2:
            raise ShortStackError("Не хватает операндов для оператора")

        right = stack.pop()
        left = stack.pop()

        if token.type is TokenType.PLUS:
            result = left + right
        elif token.type is TokenType.MINUS:
            result = left - right
        elif token.type is TokenType.STAR:
            result = left * right
        elif token.type is TokenType.SLASH:
            if right == 0:
                raise DivisionByZeroError("На ноль делить нельзя")
            result = left / right
        elif token.type is TokenType.FLOOR_DIV:
            if right == 0:
                raise DivisionByZeroError("На ноль делить нельзя")
            result = left // right
        elif token.type is TokenType.PERCENT:
            if right == 0:
                raise DivisionByZeroError("На ноль делить нельзя")
            result = left % right
        else:
            raise InvalidCharacterError(f"Неизвестный оператор: {token.value!r}")

        stack.append(result)

    if len(stack) != 1:
        raise MissingOperandError("Некорректное выражение")

    return stack[0]

def calculate(expression: str) -> int | float:
    tokens = tokenize(expression)
    tokens = _resolve_unary(tokens)
    rpn_tokens = _to_rpn(tokens)
    return _evaluate_rpn(rpn_tokens)
