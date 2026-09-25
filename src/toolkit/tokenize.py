from toolkit.constants import Token, TokenType
from toolkit.errors import EmptyExpressionError, InvalidCharacterError


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
            if i + 1 < len(expression) and expression[i + 1] == "/":
                tokens.append(Token(TokenType.FLOOR_DIV, "//"))
                i += 2
            else:
                tokens.append(Token(TokenType.SLASH, "/"))
                i += 1
            continue
        if char == "%":
            tokens.append(Token(TokenType.PERCENT, char))
            i += 1
            continue
        if char == "(":
            tokens.append(Token(TokenType.OPEN_BRACKET, char))
            i += 1
            continue
        if char == ")":
            tokens.append(Token(TokenType.CLOSE_BRACKET, char))
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
