"""
Core classes for representing p-adic elements and divisors.
"""

from typing import Dict, List, Tuple, Union
import math
from fractions import Fraction


class PadicElement:
    """
    Represents an element in a p-adic ring with its digit representation.
    """

    def __init__(self, p: int, digits: Dict[int, int] = None, valuation: int = 0):
        """
        Initialize a p-adic element.

        Args:
            p: The prime number p
            digits: Dictionary mapping position to digit (sparse representation)
            valuation: The p-adic valuation of the element
        """
        self.p = p
        self.digits = digits or {}
        self.valuation = valuation
        self._normalize()

    def _normalize(self):
        """Ensure all digits are in range [0, p-1] and handle carries."""
        # Remove zero digits for sparse representation
        self.digits = {k: v for k, v in self.digits.items() if v != 0}

        # Ensure all digits are in range [0, p-1]
        for pos in sorted(self.digits.keys()):
            if self.digits[pos] >= self.p:
                carry = self.digits[pos] // self.p
                self.digits[pos] %= self.p
                self.digits[pos + 1] = self.digits.get(pos + 1, 0) + carry

                # Remove zero digits
                if self.digits[pos] == 0:
                    del self.digits[pos]

    def get_digit(self, position: int) -> int:
        """Get the digit at the specified position."""
        return self.digits.get(self.valuation + position, 0)

    def get_digits_up_to(self, n: int) -> List[int]:
        """Get the first n digits starting from valuation."""
        return [self.get_digit(i) for i in range(n)]

    def __mul__(self, other: "PadicElement") -> "PadicElement":
        """Multiply two p-adic elements."""
        if self.p != other.p:
            raise ValueError("Elements must have the same prime p")

        result_val = self.valuation + other.valuation
        result_digits = {}

        # Compute the product using convolution
        for i, a_i in self.digits.items():
            for j, b_j in other.digits.items():
                pos = i + j - self.valuation - other.valuation
                result_digits[pos] = result_digits.get(pos, 0) + a_i * b_j

        return PadicElement(self.p, result_digits, result_val)

    def __pow__(self, exponent: Union[int, Fraction]) -> "PadicElement":
        """Raise a p-adic element to a power (integer or rational)."""
        if isinstance(exponent, int):
            if exponent == 0:
                return PadicElement(self.p, {0: 1}, 0)  # Return 1

            result = PadicElement(self.p, {0: 1}, 0)  # Start with 1
            base = PadicElement(self.p, self.digits.copy(), self.valuation)
            exp = abs(exponent)

            while exp > 0:
                if exp % 2 == 1:
                    result *= base
                base *= base
                exp //= 2

            if exponent < 0:
                # For negative exponents, we'd need inversion which requires more complexity
                raise NotImplementedError("Negative exponents not yet implemented")

            return result

        elif isinstance(exponent, Fraction):
            # For rational exponents, we need a more sophisticated approach
            # This is a simplified implementation that works for units with valuation 0
            if self.valuation != 0:
                raise ValueError("Rational powers currently only supported for units")

            # Convert to the form x^(n/d)
            n, d = exponent.numerator, exponent.denominator

            # Check if p^(1/d) makes sense in our context
            if d != self.p:
                raise NotImplementedError(
                    f"Only 1/{self.p} powers are currently implemented"
                )

            # Create a new approximation with fractional valuation
            # This is a simplified version that works for demo purposes
            new_digits = {0: 1}  # Approximate by 1 + correction terms
            for i in range(1, 10):  # Add several correction terms
                new_digits[i] = (self.get_digit(i) * n) % self.p

            result = PadicElement(self.p, new_digits, 0)
            return result

        else:
            raise TypeError("Exponent must be an integer or Fraction")

    def __str__(self) -> str:
        """String representation of the p-adic element."""
        if not self.digits:
            return "0"

        terms = []
        for pos, digit in sorted(self.digits.items()):
            power = pos - self.valuation
            if power == 0:
                terms.append(str(digit))
            else:
                terms.append(f"{digit}·p^{power}")

        return " + ".join(terms) or "0"


class Divisor:
    """
    Represents a prime divisor in a ring.
    """

    def __init__(self, name: str):
        """
        Initialize a prime divisor.

        Args:
            name: Name/identifier of the divisor
        """
        self.name = name

    def __str__(self) -> str:
        """String representation of the divisor."""
        return f"div({self.name})"


class QDivisor:
    """
    Represents a Q-divisor (sum of prime divisors with rational coefficients).
    """

    def __init__(self, components: Dict[Divisor, Fraction]):
        """
        Initialize a Q-divisor.

        Args:
            components: Dictionary mapping prime divisors to rational coefficients
        """
        self.components = components

    def __add__(self, other: "QDivisor") -> "QDivisor":
        """Add two Q-divisors."""
        result = self.components.copy()
        for div, coef in other.components.items():
            result[div] = result.get(div, Fraction(0)) + coef
        return QDivisor(result)

    def compute_threshold(self) -> int:
        """Compute the valuation threshold t_Δ for this divisor."""
        if not self.components:
            return float("inf")

        return math.ceil(min(1 / coef for coef in self.components.values()))

    def compute_epsilon_values(self) -> Dict[Divisor, float]:
        """Compute epsilon values for each component."""
        result = {}
        for div, coef in self.components.items():
            n, m = coef.numerator, coef.denominator
            m_log = math.ceil(math.log(m, self.p if hasattr(self, "p") else 2))
            epsilon = n / (m * pow(self.p if hasattr(self, "p") else 2, m_log))
            result[div] = epsilon
        return result

    def compute_weights(self, position: int, p: int) -> float:
        """Compute the weight w_i(Δ) for a specific position."""
        epsilons = self.compute_epsilon_values()
        return sum(
            coef * pow(p, -position * epsilons[div])
            for div, coef in self.components.items()
        )

    def compute_complexity_bound(self) -> float:
        """Compute the complexity bound C_Δ."""
        result = 0
        coeffs = list(self.components.values())
        for i, c_i in enumerate(coeffs):
            n_i, m_i = c_i.numerator, c_i.denominator
            delta_i = sum(
                Fraction(c_j.numerator, c_j.denominator)
                * math.gcd(m_i, c_j.denominator)
                / m_i
                for c_j in coeffs
            )
            result += float(c_i * (1 + delta_i))
        return result

    def __str__(self) -> str:
        """String representation of the Q-divisor."""
        terms = []
        for div, coef in self.components.items():
            terms.append(f"{coef} · {div}")
        return " + ".join(terms) or "0"
