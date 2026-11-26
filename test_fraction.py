import operator

import pytest

from fraction import Fraction


def test_initialization_reduces_fraction():
    # Check that the constructor simplifies the fraction and keeps its sign.
    fraction = Fraction(-6, 8)
    assert (fraction.numerator, fraction.denominator) == (-3, 4)


def test_zero_is_reduced_to_zero_over_one():
    fraction = Fraction(0, 5)
    assert (fraction.numerator, fraction.denominator) == (0, 1)


# pytest runs the test once for each pair of invalid inputs.
@pytest.mark.parametrize("numerator, denominator", [(1.0, 2), (1, "2"), (True, 2)])
def test_rejects_non_integers(numerator, denominator):
    with pytest.raises(TypeError):
        Fraction(numerator, denominator)


@pytest.mark.parametrize("denominator", [0, -2])
def test_rejects_non_positive_denominator(denominator):
    with pytest.raises(ValueError):
        Fraction(1, denominator)


# Test each of the six comparison operators.
@pytest.mark.parametrize(
    "compare, expected",
    [
        (operator.eq, (False, True, False)),
        (operator.ne, (True, False, True)),
        (operator.lt, (True, False, False)),
        (operator.le, (True, True, False)),
        (operator.gt, (False, False, True)),
        (operator.ge, (False, True, True)),
    ],
)
def test_comparisons(compare, expected):
    half = Fraction(1, 2)

    # The three values are less than, equal to, and greater than 1/2.
    values = [Fraction(-1, 3), Fraction(2, 4), Fraction(3, 4)]
    assert tuple(compare(value, half) for value in values) == expected


# Test the four additional special methods.
def test_str():
    assert str(Fraction(2, 4)) == "1/2"


def test_repr():
    assert repr(Fraction(2, 4)) == "Fraction(1, 2)"


def test_negation():
    assert -Fraction(1, 2) == Fraction(-1, 2)


def test_addition():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)


def test_unrelated_operand():
    # A string compares unequal. Ordering and addition raise TypeError.
    fraction = Fraction(1, 2)
    assert fraction != "1/2"

    with pytest.raises(TypeError):
        fraction < "1/2"

    with pytest.raises(TypeError):
        fraction + "1/2"
