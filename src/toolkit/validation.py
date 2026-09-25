from toolkit.constants import _BINARY_TYPES, _PRECEDENCE, Token, TokenType
from toolkit.errors import (
    ConsecutiveOperatorError,
    MissingOperandError,
    UnbalancedParenthesesError,
)


def _resolve_unary(tokens: list[Token]) -> list[Token]:
    """Переклассифицировать PLUS/MINUS в NEG/POS там, где они унарные."""
    resolved: list[Token] = []
    previous: Token | None = None

    for token in tokens:
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            is_unary = (
                previous is None
                or previous.type in (
                    TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
                    TokenType.SLASH, TokenType.FLOOR_DIV, TokenType.PERCENT,
                    TokenType.OPEN_BRACKET, TokenType.NEG, TokenType.POS,
                )
            )
            if is_unary:
                new_type = TokenType.NEG if token.type is TokenType.MINUS else TokenType.POS
                new_token = Token(new_type, token.value)
                resolved.append(new_token)
                previous = new_token
                continue

        if token.type in _BINARY_TYPES:
            if previous is not None and previous.type in _BINARY_TYPES:
                raise ConsecutiveOperatorError(f"Два бинарных оператора подряд: "
                                               f"{previous!r} и {token.value!r}")
            if (previous is None
                or previous.type is TokenType.OPEN_BRACKET
                or previous.type in (TokenType.NEG, TokenType.POS)):
                raise MissingOperandError(f"Не хватает операнда перед {token.value!r}")

        if token.type is TokenType.CLOSE_BRACKET:
            if previous is not None and previous.type is TokenType.OPEN_BRACKET:
                raise MissingOperandError("Пустые скобки")
            if previous is not None and previous.type in (TokenType.NEG, TokenType.POS):
                raise MissingOperandError(f"Не хватает операнда перед {token.value!r}")

        resolved.append(token)
        previous = token

    if previous is not None and (
        previous.type in _BINARY_TYPES
        or previous.type in (TokenType.NEG, TokenType.POS)
        or previous.type is TokenType.OPEN_BRACKET
    ):
        raise MissingOperandError("Выражение обрывается оператором")

    return resolved

def _to_rpn(tokens: list[Token]) -> list[Token]:
    output: list[Token] = []
    operator_stack: list[Token] = []

    for token in tokens:
        if token.type is TokenType.NUMBER:
            output.append(Token(TokenType.NUMBER, token.value))

        elif token.type in _PRECEDENCE:
            while (
                operator_stack
                and operator_stack[-1].type in _PRECEDENCE
                and _PRECEDENCE[operator_stack[-1].type] >= _PRECEDENCE[token.type]
            ):
                output.append(operator_stack.pop())
            operator_stack.append(token)

        elif token.type is TokenType.OPEN_BRACKET:
            operator_stack.append(Token(TokenType.OPEN_BRACKET, token.value))

        elif token.type is TokenType.CLOSE_BRACKET:
            while (
                operator_stack and operator_stack[-1].type is not TokenType.OPEN_BRACKET
            ):
                output.append(operator_stack.pop())
            if not operator_stack:
                raise UnbalancedParenthesesError("Не хватает открывающей скобки")
            operator_stack.pop()

    while operator_stack:
        if operator_stack[-1].type is TokenType.OPEN_BRACKET:
            raise UnbalancedParenthesesError("Не хватает закрывающей скобки")
        output.append(operator_stack.pop())

    return output
