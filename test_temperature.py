import pytest

from temperature import Temperature

# (Celsius, Fahrenheit, Kelvin) reference points
REFERENCE_POINTS = [
    (-273.15, -459.67, 0.0),    # absolute zero
    (-40.0, -40.0, 233.15),     # Celsius-Fahrenheit crossover
    (0.0, 32.0, 273.15),        # freezing point of water
    (37.0, 98.6, 310.15),       # human body temperature
    (100.0, 212.0, 373.15),     # boiling point of water
]


# 1. Initialization
def test_default_unit_is_celsius() -> None:
    assert Temperature(25).unit == "C"


@pytest.mark.parametrize("unit", ["c", "f", "k", "C", "F", "K"])
def test_units_are_case_insensitive(unit: str) -> None:
    assert Temperature(300, unit).unit == unit.upper()


def test_value_and_unit_are_read_only() -> None:
    t = Temperature(25, "C")
    with pytest.raises(AttributeError):
        t.value = 30  # type: ignore[misc]
    with pytest.raises(AttributeError):
        t.unit = "F"  # type: ignore[misc]


# 2. Validation
@pytest.mark.parametrize("unit", ["X", "", "Celsius", "CF"])
def test_invalid_unit_raises(unit: str) -> None:
    with pytest.raises(ValueError):
        Temperature(10, unit)


@pytest.mark.parametrize("value, unit", [(-273.16, "C"), (-459.68, "F"), (-0.01, "K")])
def test_below_absolute_zero_raises(value: float, unit: str) -> None:
    with pytest.raises(ValueError):
        Temperature(value, unit)


@pytest.mark.parametrize("value, unit", [(-273.15, "C"), (-459.67, "F"), (0, "K")])
def test_absolute_zero_is_allowed(value: float, unit: str) -> None:
    Temperature(value, unit)


def test_convert_to_invalid_unit_raises() -> None:
    with pytest.raises(ValueError):
        Temperature(10, "C").convert_to("X")


# 3. Conversions
@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_celsius(c: float, f: float, k: float) -> None:
    t = Temperature(c, "C")
    assert t.to_celsius() == pytest.approx(c, abs=1e-9)
    assert t.to_fahrenheit() == pytest.approx(f, abs=1e-9)
    assert t.to_kelvin() == pytest.approx(k, abs=1e-9)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_fahrenheit(c: float, f: float, k: float) -> None:
    t = Temperature(f, "F")
    assert t.to_celsius() == pytest.approx(c, abs=1e-9)
    assert t.to_fahrenheit() == pytest.approx(f, abs=1e-9)
    assert t.to_kelvin() == pytest.approx(k, abs=1e-9)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_kelvin(c: float, f: float, k: float) -> None:
    t = Temperature(k, "K")
    assert t.to_celsius() == pytest.approx(c, abs=1e-9)
    assert t.to_fahrenheit() == pytest.approx(f, abs=1e-9)
    assert t.to_kelvin() == pytest.approx(k, abs=1e-9)


def test_convert_to_returns_new_instance() -> None:
    original = Temperature(100, "C")
    converted = original.convert_to("f")
    assert converted.unit == "F"
    assert converted.value == pytest.approx(212.0)
    assert original.unit == "C"


# 4. Round trips
@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_round_trip_c_f_k_c(c: float, f: float, k: float) -> None:
    original = Temperature(c, "C")
    result = original.convert_to("F").convert_to("K").convert_to("C")
    assert result.unit == "C"
    assert result.value == pytest.approx(original.value, abs=1e-9)
    assert result == original


# 5. Comparisons
def test_equality_across_units() -> None:
    assert Temperature(0, "C") == Temperature(32, "F")
    assert Temperature(0, "C") == Temperature(273.15, "K")
    assert Temperature(100, "C") == Temperature(212, "F")


def test_equality_uses_tolerance() -> None:
    assert Temperature(25, "C") == Temperature(25 + 1e-10, "C")
    assert Temperature(25, "C") != Temperature(25.001, "C")


def test_ordering_across_units() -> None:
    cold, warm = Temperature(0, "C"), Temperature(100, "F")
    assert cold < warm
    assert cold <= warm
    assert warm > cold
    assert warm >= cold
    assert not warm < cold
    assert Temperature(0, "C") <= Temperature(32, "F")
    assert Temperature(0, "C") >= Temperature(32, "F")
    assert not Temperature(0, "C") < Temperature(32, "F")


def test_not_equal() -> None:
    assert Temperature(0, "C") != Temperature(0, "F")


def test_comparison_with_other_types_is_not_implemented() -> None:
    t = Temperature(0, "C")
    assert t.__eq__(5) is NotImplemented
    assert t.__ne__(5) is NotImplemented
    assert t.__lt__(5) is NotImplemented
    assert t.__le__(5) is NotImplemented
    assert t.__gt__(5) is NotImplemented
    assert t.__ge__(5) is NotImplemented
    assert t != 5
    with pytest.raises(TypeError):
        t < 5


# 6. Formatting
def test_str_has_two_decimals() -> None:
    assert str(Temperature(25, "C")) == "25.00 °C"
    assert str(Temperature(98.6, "F")) == "98.60 °F"
    assert str(Temperature(273.15, "K")) == "273.15 K"


def test_repr_is_unambiguous() -> None:
    assert repr(Temperature(25, "c")) == "Temperature(25.0, 'C')"