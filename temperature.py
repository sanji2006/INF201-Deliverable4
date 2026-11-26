from __future__ import annotations

TOLERANCE = 1e-9
_VALID_UNITS = ("C", "F", "K")


def _to_kelvin(value: float, unit: str) -> float:
    """Convert a value in the given unit (C, F or K) to Kelvin."""
    if unit == "C":
        return value + 273.15
    if unit == "F":
        return (value - 32) * 5 / 9 + 273.15
    return value


def _from_kelvin(kelvin: float, unit: str) -> float:
    """Convert a Kelvin value to the given unit (C, F or K)."""
    if unit == "C":
        return kelvin - 273.15
    if unit == "F":
        return (kelvin - 273.15) * 9 / 5 + 32
    return kelvin


class Temperature:
    """A temperature in Celsius, Fahrenheit or Kelvin."""

    def __init__(self, value: float, unit: str = "C") -> None:
        if not isinstance(unit, str) or unit.upper() not in _VALID_UNITS:
            raise ValueError(f"Unit must be one of 'C', 'F' or 'K', got {unit!r}.")
        unit = unit.upper()
        value = float(value)
        # The tolerance avoids rejecting absolute zero because of rounding errors
        if _to_kelvin(value, unit) < -TOLERANCE:
            raise ValueError("Temperature cannot be below absolute zero (0 K).")
        self._value = value
        self._unit = unit

    @property
    def value(self) -> float:
        """Read-only temperature value."""
        return self._value

    @property
    def unit(self) -> str:
        """Read-only unit, always upper case."""
        return self._unit

    def _kelvin(self) -> float:
        return _to_kelvin(self._value, self._unit)

    def to_celsius(self) -> float:
        return _from_kelvin(self._kelvin(), "C")

    def to_fahrenheit(self) -> float:
        return _from_kelvin(self._kelvin(), "F")

    def to_kelvin(self) -> float:
        return self._kelvin()

    def convert_to(self, target_unit: str) -> Temperature:
        """Return a new Temperature in the target unit (case-insensitive)."""
        if not isinstance(target_unit, str) or target_unit.upper() not in _VALID_UNITS:
            raise ValueError(f"Unit must be one of 'C', 'F' or 'K', got {target_unit!r}.")
        target_unit = target_unit.upper()
        return Temperature(_from_kelvin(self._kelvin(), target_unit), target_unit)

    def __repr__(self) -> str:
        return f"Temperature({self._value!r}, {self._unit!r})"

    def __str__(self) -> str:
        symbol = "K" if self._unit == "K" else f"°{self._unit}"
        return f"{self._value:.2f} {symbol}"

    # Comparisons are done in Kelvin, with a tolerance for floating-point errors
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return abs(self._kelvin() - other._kelvin()) <= TOLERANCE

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self == other

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin() < other._kelvin() - TOLERANCE

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin() <= other._kelvin() + TOLERANCE

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin() > other._kelvin() + TOLERANCE

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin() >= other._kelvin() - TOLERANCE

    __hash__ = None  # type: ignore[assignment]  # tolerance-based equality is not hashable