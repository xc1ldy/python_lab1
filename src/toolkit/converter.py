from toolkit.constants import _ABSOLUTE_ZERO, _LENGTH_TO_METERS, _MASS_TO_GRAMS
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


def _unit_group(unit: str) -> str:
    if unit in _LENGTH_TO_METERS:
        return "length"
    if unit in _MASS_TO_GRAMS:
        return "mass"
    if unit in ("c", "f", "k"):
        return "temperature"
    raise UnknownUnitError(f"Неизвестная единица: {unit!r}")

def _to_celsius(unit: str, value: float) -> float:
    if unit == 'c':
        return value
    if unit == 'f':
        return (value - 32) * 5/9
    return value - 273.15 # unit == "k"

def _from_celsius(unit: str, celsius: float) -> float:
    if unit == 'c':
        return celsius
    if unit == 'f':
        return celsius * 9/5 + 32
    return celsius + 273.15 # unit == "k"

def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    from_group = _unit_group(from_unit)
    to_group = _unit_group(to_unit)

    if from_group != to_group:
        raise IncompatibleUnitsError(
            f"Нельзя конвертировать {from_group!r} в {to_group!r}"
        )

    if from_group == "temperature":
        if value < _ABSOLUTE_ZERO[from_unit]:
            raise BelowAbsoluteZeroError("Ниже абсолютного нуля")
        temperature = _to_celsius(from_unit, value)
        return float(_from_celsius(to_unit, temperature))

    if from_group == "length":
        meters = value * _LENGTH_TO_METERS[from_unit]
        return float(meters / _LENGTH_TO_METERS[to_unit])

    else:
        grams = value * _MASS_TO_GRAMS[from_unit]
        return float(grams / _MASS_TO_GRAMS[to_unit])
