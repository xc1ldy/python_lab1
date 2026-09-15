class ToolkitError(Exception):
    """Базовая ошибка для всего проекта."""


class EmptyExpressionError(ToolkitError):
    """Выражение пустое."""


class InvalidCharacterError(ToolkitError):
    """Встретился недопустимый символ."""


class MissingOperandError(ToolkitError):
    """Не хватает числа (операнда)."""


class ConsecutiveOperatorError(ToolkitError):
    """Два оператора подряд."""


class DivisionByZeroError(ToolkitError):
    """Деление на ноль."""

class UnknownUnitError(ToolkitError):
    """Единица не найдена ни в одной группе."""


class IncompatibleUnitsError(ToolkitError):
    """Единицы принадлежат разным группам."""


class BelowAbsoluteZeroError(ToolkitError):
    """Температура ниже абсолютного нуля."""

class InvalidNumberError(ToolkitError):
    """Числовая ошибка ввода."""
