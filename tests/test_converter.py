import pytest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


def test_length_mm_to_m() -> None:
    assert abs(convert(1000, "mm", "m") - 1.0) < 0.000001


def test_mass_kg_to_g() -> None:
    assert abs(convert(2, "kg", "g") - 2000.0) < 0.000001


def test_temperature_c_to_f() -> None:
    assert abs(convert(0, "c", "f") - 32.0) < 0.000001


def test_units_are_case_insensitive() -> None:
    assert abs(convert(1, "KM", "M") - 1000.0) < 0.000001


def test_result_is_always_float() -> None:
    assert isinstance(convert(5, "g", "g"), float)


def test_unknown_unit_raises() -> None:
    with pytest.raises(UnknownUnitError):
        convert(1, "banana", "m")


def test_incompatible_units_raise() -> None:
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "m", "kg")


def test_below_absolute_zero_raises() -> None:
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-300, "c", "f")
