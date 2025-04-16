#!/usr/bin/env python
"""
Test script to validate the binary p-adic predicate implementation.
"""
import math
from fractions import Fraction
from padiclib import (
    PadicElement,
    Divisor,
    QDivisor,
    BinaryPredicate,
    test_ideal_membership,
    subadditivity_factorization,
    FormulationClassifier,
)


def test_padic_arithmetic():
    """Test p-adic element arithmetic."""
    print("Testing p-adic arithmetic:")

    # Create some p-adic elements (p=5)
    a = PadicElement(5, {0: 2, 1: 3}, 0)  # 2 + 3·5
    b = PadicElement(5, {0: 1, 2: 4}, 0)  # 1 + 4·5²

    # Multiplication
    c = a * b
    expected_c_digits = {0: 2, 1: 3, 2: 8, 3: 12}  # 2·1 + (2·4·5² + 3·5·1) + 3·5·4·5²
    print(f"  a = {a}")
    print(f"  b = {b}")
    print(f"  a * b = {c}")

    # Power
    d = PadicElement(5, {0: 2}, 0)  # 2
    d_squared = d**2
    print(f"  {d}² = {d_squared}")

    # Fractional power (simplified approximation)
    try:
        d_frac = d ** Fraction(1, 5)
        print(f"  {d}^(1/5) ≈ {d_frac}")
    except NotImplementedError:
        print("  Fractional powers not fully implemented")

    print()


def create_standard_predicate(p, threshold, complexity):
    """Create a standard test ideal predicate."""

    def predicate_func(element, t):
        # 1. Check valuation condition
        if element.valuation >= threshold:
            return True

        # 2. Count non-zero digits and weight them
        weighted_sum = 0
        digits = element.get_digits_up_to(t + 10)  # Get sufficient digits

        for i, digit in enumerate(digits):
            if digit != 0:
                # Simple weighting: earlier digits have higher weight
                weighted_sum += p ** (-i / 2)

        # 3. Compare weighted sum to complexity bound
        return weighted_sum < complexity

    return BinaryPredicate(predicate_func, p)


def test_divisor_predicate():
    """Test predicates defined by divisors."""
    print("Testing divisor-based predicates:")

    # Create a simple Q-divisor with two components
    D1 = Divisor("D1")
    D2 = Divisor("D2")
    components = {D1: Fraction(2, 3), D2: Fraction(3, 5)}  # 2/3 D1  # 3/5 D2
    divisor = QDivisor(components)

    # Compute parameters
    threshold = divisor.compute_threshold()
    complexity = divisor.compute_complexity_bound()

    print(f"  Divisor: {divisor}")
    print(f"  Threshold t_Δ: {threshold}")
    print(f"  Complexity bound C_Δ: {complexity}")

    # Create a predicate from this divisor
    p = 5

    def divisor_predicate(element, t):
        # Implement the binary predicate from the paper
        # P_Δ(bin_p(x)) = (val(x) < t_Δ) ∧ (∑ w_i(Δ)·φ(a_i) < C_Δ)

        # 1. Check valuation condition
        if element.valuation >= threshold:
            return False

        # 2. Compute weighted sum with weights w_i(Δ)
        weighted_sum = 0
        truncation_bound = math.ceil(20)  # Sufficient for demonstration

        for i in range(truncation_bound):
            digit = element.get_digit(i)
            if digit != 0:
                weight = divisor.compute_weights(i, p)
                weighted_sum += weight

        # 3. Check complexity condition
        return weighted_sum < complexity

    predicate = BinaryPredicate(divisor_predicate, p, divisor)

    # Test some elements
    elements = [
        PadicElement(p, {0: 1}, 0),  # 1
        PadicElement(p, {0: 2, 1: 3}, 0),  # 2 + 3·5
        PadicElement(p, {}, 2),  # 5²
        PadicElement(p, {i: 1 for i in range(5)}, 0),  # 1 + 1·5 + 1·5² + 1·5³ + 1·5⁴
    ]

    print("\n  Testing membership:")
    for i, elem in enumerate(elements):
        result = predicate.test_ideal(elem, 2)
        print(f"  Element {i+1}: {elem} in test ideal? {result}")

    print()


def test_subadditivity():
    """Test subadditivity factorization."""
    print("Testing subadditivity factorization:")

    p = 5

    # Create two simple predicates
    pred1 = create_standard_predicate(p, 2, 1.5)
    pred2 = create_standard_predicate(p, 3, 2.0)

    # Create divisors for more precise behavior
    D1 = Divisor("D1")
    D2 = Divisor("D2")

    div1 = QDivisor({D1: Fraction(1, 2)})
    div2 = QDivisor({D2: Fraction(2, 3)})

    pred1.divisor = div1
    pred2.divisor = div2

    # Get combined predicate and bound
    combined_pred, bound = subadditivity_factorization(pred1, pred2)

    print(f"  Predicate 1: threshold={pred1.divisor.compute_threshold()}")
    print(f"  Predicate 2: threshold={pred2.divisor.compute_threshold()}")
    print(f"  Combined divisor: {combined_pred.divisor}")
    print(f"  Subadditivity bound C: {bound}")

    # Test an element
    x = PadicElement(p, {0: 3, 1: 2, 3: 1}, 0)

    # Check if x is in the test ideal of the combined predicate
    combined_result = test_ideal_membership(combined_pred, x, 5)

    # Try to find a factorization
    factorization_found = False
    for i in range(p):
        for j in range(p):
            y = PadicElement(p, {0: i}, 0)
            z = PadicElement(p, {0: j}, 0)

            if y * z == x:  # Simplified check
                y_result = test_ideal_membership(pred1, y, 2)
                z_result = test_ideal_membership(pred2, z, 3)

                if y_result and z_result:
                    factorization_found = True
                    print(f"\n  Found factorization: {x} = {y} × {z}")
                    print(f"  {y} in test ideal 1? {y_result}")
                    print(f"  {z} in test ideal 2? {z_result}")
                    break

        if factorization_found:
            break

    if not factorization_found:
        print("\n  No simple factorization found")

    print(f"  Element in combined test ideal? {combined_result}")
    print()


def test_formulation_classifier():
    """Test the formulation classifier."""
    print("Testing formulation classifier:")

    p = 5
    classifier = FormulationClassifier(p)

    # Register different formulations
    # 1. Standard formulation
    def standard_pred(element, t):
        if element.valuation >= 2:
            return True
        weighted_sum = sum(
            1.0 * p ** (-i)
            for i, d in enumerate(element.get_digits_up_to(t + 5))
            if d != 0
        )
        return weighted_sum < 2.0

    # 2. Alternate formulation (with different weighting)
    def alt_pred(element, t):
        if element.valuation >= 2:
            return True
        weighted_sum = sum(
            0.8 * p ** (-i * 0.8)
            for i, d in enumerate(element.get_digits_up_to(t + 5))
            if d != 0
        )
        return weighted_sum < 1.6

    # 3. Very different formulation
    def different_pred(element, t):
        if element.valuation >= 4:  # Different threshold
            return True
        weighted_sum = sum(
            0.5 * p ** (-i * 0.5)
            for i, d in enumerate(element.get_digits_up_to(t + 5))
            if d != 0
        )
        return weighted_sum < 1.0

    # Register formulations
    classifier.register_formulation("standard", BinaryPredicate(standard_pred, p))
    classifier.register_formulation("alternate", BinaryPredicate(alt_pred, p))
    classifier.register_formulation("different", BinaryPredicate(different_pred, p))

    # Test equivalence
    std_alt_equiv = classifier.are_equivalent("standard", "alternate")
    std_diff_equiv = classifier.are_equivalent("standard", "different")

    print(f"  'standard' and 'alternate' equivalent? {std_alt_equiv}")
    print(f"  'standard' and 'different' equivalent? {std_diff_equiv}")

    # Create a new predicate and find equivalent formulations
    def new_pred(element, t):
        if element.valuation >= 2:
            return True
        weighted_sum = sum(
            1.0 * p ** (-i)
            for i, d in enumerate(element.get_digits_up_to(t + 5))
            if d != 0
        )
        return weighted_sum < 1.9  # Slightly different bound

    new_predicate = BinaryPredicate(new_pred, p)

    equivalents = classifier.find_equivalent_formulations(new_predicate)
    print(f"  Formulations equivalent to new predicate: {equivalents}")
    print()


def main():
    """Run all tests."""
    print("====== Binary P-adic Predicate Testing ======\n")

    test_padic_arithmetic()
    test_divisor_predicate()
    test_subadditivity()
    test_formulation_classifier()

    print("All tests completed.")


if __name__ == "__main__":
    main()
