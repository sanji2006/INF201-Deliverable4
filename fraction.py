from __future__ import annotations

from functools import total_ordering
from math import gcd


# Python uses __eq__ and __lt__ to supply <=, >, and >=.
# The default implementation of != uses __eq__.
@total_ordering
class Fraction:
    """Represent a fraction with a positive denominator."""

    def __init__(self, numerator: int, denominator: int) -> None:
        # Require actual integers. This also rejects True and False.
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("Numerator and denominator must be integers.")

        if denominator <= 0:
            raise ValueError("Denominator must be greater than zero.")

        # Divide both parts by their greatest common divisor.
        # For example, 6/8 becomes 3/4.
        divisor = gcd(numerator, denominator)
        self._numerator = numerator // divisor
        self._denominator = denominator // divisor

    # Properties let callers read the simplified values.
    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented

        # Equivalent fractions have identical parts after simplification.
        return (self.numerator, self.denominator) == (
            other.numerator, other.denominator
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented

        # Compare a/b and c/d by comparing a*d and c*b.
        # Both denominators are positive, so the inequality keeps its direction.
        return self.numerator * other.denominator < (
            other.numerator * self.denominator
        )

    def __str__(self) -> str:
        # Format used by print(fraction), for example "1/2".
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        # Show how to construct the fraction, for example "Fraction(1, 2)".
        return f"Fraction({self.numerator}, {self.denominator})"

    def __neg__(self) -> Fraction:
        # Applying a minus sign changes the numerator's sign.
        return Fraction(-self.numerator, self.denominator)

    def __add__(self, other: object) -> Fraction:
        if not isinstance(other, Fraction):
            return NotImplemented

        # Add a/b and c/d using the common denominator b*d.
        numerator = (
            self.numerator * other.denominator
            + other.numerator * self.denominator
        )
        denominator = self.denominator * other.denominator

        # The constructor simplifies the result automatically.
        return Fraction(numerator, denominator)
