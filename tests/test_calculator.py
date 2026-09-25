import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    ConsecutiveOperatorError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
)


def test_addition() -> None:
    assert calculate("2 + 3") == 5

def test_subtraction() -> None:
    assert calculate("10 - 4") == 6

def test_multiplication() -> None:
    assert calculate("3 * 4") == 12

def test_division() -> None:
    assert calculate("9 / 2") == 4.5

def test_minus() -> None:
    assert calculate("-5 + 2") == -3

def test_operator_precedence() -> None:
    assert calculate("2 + 3 * 4") == 14

def test_equals() -> None:
    assert calculate("4") == 4

def test_invalid_character_error() -> None:
    with pytest.raises(InvalidCharacterError):
        calculate("2 + a")

def test_missing_operand_error() -> None:
    with pytest.raises(MissingOperandError):
        calculate("2 +")

def test_consecutive_operator_error() -> None:
    with pytest.raises(ConsecutiveOperatorError):
        calculate("2 * / 3")


def test_division_by_zero() -> None:
    with pytest.raises(DivisionByZeroError):
        calculate("5 / 0")

def test_empty_expression_error() -> None:
    with pytest.raises(EmptyExpressionError):
        calculate("")
