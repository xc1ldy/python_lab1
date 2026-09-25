from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto() # число
    PLUS = auto() # плюс
    MINUS = auto() # минус
    STAR = auto() # умножение
    SLASH = auto() # деление
    FLOOR_DIV = auto() # целочисленное деление
    PERCENT = auto() # остаток от деления
    OPEN_BRACKET = auto() # открывающая скобка
    CLOSE_BRACKET = auto() # закрывающая скобка
    NEG = auto() # унарный минус
    POS = auto() # унарный плюс

@dataclass
class Token:
    type: TokenType
    value: str


_ABSOLUTE_ZERO = {
    "c": -273.15,
    "k": 0.0,
    "f": -459.67
}

_LENGTH_TO_METERS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

_MASS_TO_GRAMS = {
    "g": 1.0,
    "kg": 1000.0,
}

_BINARY_TYPES = {
    TokenType.PLUS,
    TokenType.MINUS,
    TokenType.STAR,
    TokenType.SLASH,
    TokenType.FLOOR_DIV,
    TokenType.PERCENT,
}

_PRECEDENCE = {
    TokenType.PLUS: 1,
    TokenType.MINUS: 1,
    TokenType.STAR: 2,
    TokenType.SLASH: 2,
    TokenType.FLOOR_DIV: 2,
    TokenType.PERCENT: 2,
    TokenType.NEG: 3,
    TokenType.POS: 3,
}
