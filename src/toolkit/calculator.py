from dataclasses import dataclass
from enum import Enum, auto

from toolkit.errors import (
    ConsecutiveOperatorError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
)


class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()


@dataclass
class Token:
    type: TokenType
    value: str


def tokenize(expression: str) -> list[Token]:
    if not expression.strip():
        raise EmptyExpressionError("Пустое выражение")
    tokens: list[Token] = []
    i = 0
    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue
        if char == "+":
            tokens.append(Token(TokenType.PLUS, char))
            i += 1
            continue
        if char == "-":
            tokens.append(Token(TokenType.MINUS, char))
            i += 1
            continue
        if char == "*":
            tokens.append(Token(TokenType.STAR, char))
            i += 1
            continue
        if char == "/":
            tokens.append(Token(TokenType.SLASH, char))
            i += 1
            continue

        if char.isdigit():
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            tokens.append(Token(TokenType.NUMBER, expression[start:i]))
            continue

        raise InvalidCharacterError(f"Недопустимый символ: {char!r}")

    return tokens

class _Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> Token | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _advance(self) -> Token:
        token = self._tokens[self._pos]
        self._pos += 1
        return token


    def _parse_factor(self):
        token = self._peek()
        if token is None:
            raise MissingOperandError("Ожидалось число")

        if token.type in (TokenType.STAR, TokenType.SLASH):
            raise ConsecutiveOperatorError(f"Неожиданный оператор {token.value!r}.")

        sign = 1
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self._advance()
            sign = 1 if token.type == TokenType.PLUS else -1
            token = self._peek()
            if token is None:
                raise MissingOperandError("Ожидалось число")
            if token.type is not TokenType.NUMBER:
                raise ConsecutiveOperatorError(f"Неожиданный оператор {token.value!r}.")

        number_token = self._advance()
        if "." in number_token.value:
            value = float(number_token.value)
        else:
            value = int(number_token.value)
        return sign * value


    def _parse_term(self):
        value = self._parse_factor()

        while self._peek() is not None and self._peek().type in (TokenType.STAR, TokenType.SLASH):
            operator = self._advance()
            right = self._parse_factor()

            if operator.type is TokenType.STAR:
                value = value * right
            elif right == 0:
                raise DivisionByZeroError("На ноль делить нельзя")
            else:
                value = value / right
        return value


    def _parse_expression(self):
        value = self._parse_term()  # шаг 1: первый "term"

        while self._peek() is not None and self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self._advance()
            right = self._parse_term()

            if operator.type is TokenType.PLUS:
                value = value + right
            else:
                value = value - right

        return value


    def parse(self):
        result = self._parse_expression()
        if self._peek() is not None:
            raise MissingOperandError(f"Лишний токен после выражения: {self._peek().value!r}")
        return result

def calculate(expression: str):
    tokens = tokenize(expression)
    return _Parser(tokens).parse()
