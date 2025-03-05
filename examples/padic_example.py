#!/usr/bin/env python3
"""
Example script demonstrating the usage of the padicmath library.

This script provides examples of:
1. Creating and manipulating p-adic numbers
2. Working with binary p-adic numbers and test ideals
3. Testing mathematical properties and formulas
4. Running verification analysis of the binary p-adic test ideal theory
"""
import sys
import os

# Add the parent directory to sys.path to import the local package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from padicmath import (
    PAdicNumber, 
    BinaryPAdicNumber,
    rational_to_padic,
    rational_to_binary_padic,
    padic_valuation,
    is_in_test_ideal,
    compare_test_ideals,
    generate_test_cases,
    perfectoid_factorization_predicate,
    test_subadditivity_counterexamples,
    verify_binary_predicate_properties,
    BinaryPAdicVerifier
)


def example_padic_basics():
    """Example of basic p-adic number operations."""
    print("\n=== P-adic Number Basics ===")
    
    # Create p-adic numbers
    p_adic1 = PAdicNumber([1, 2, 3], prime=5)
    p_adic2 = PAdicNumber([3, 4, 1], prime=5)
    
    print(f"p_adic1 = {p_adic1}")
    print(f"p_adic2 = {p_adic2}")
    
    # Addition
    sum_result = p_adic1 + p_adic2
    print(f"p_adic1 + p_adic2 = {sum_result}")
    
    # Multiplication
    product_result = p_adic1 * p_adic2
    print(f"p_adic1 * p_adic2 = {product_result}")
    
    # Convert from rational
    rational_padic = rational_to_padic(7, 3, prime=5, precision=10)
    print(f"7/3 as p-adic (base 5): {rational_padic}")
    
    # P-adic valuation
    print(f"val_5(125) = {padic_valuation(125, 5)}")


def example_binary_padic():
    """Example of binary p-adic numbers and test ideals."""
    print("\n=== Binary P-adic Numbers and Test Ideals ===")
    
    # Create a binary p-adic number
    bin_padic = BinaryPAdicNumber([1, 2, 0, 4, 3], prime=5)
    print(f"Binary p-adic: {bin_padic}")
    print(f"Original digits: {bin_padic.digits}")
    print(f"Binary digits: {bin_padic.binary_digits}")
    
    # Test ideal membership with different coefficients
    for coef in [0.1, 0.3, 0.5, 0.7, 0.9]:
        is_member = is_in_test_ideal(bin_padic, coef)
        print(f"Test ideal membership with coefficient {coef}: {is_member}")
    
    # Convert a rational number to binary p-adic
    bin_rational = rational_to_binary_padic(7, 3, prime=5, precision=10)
    print(f"7/3 as binary p-adic: {bin_rational}")
    print(f"Binary digits: {bin_rational.binary_digits}")
    
    # Check if the number admits perfectoid factorization
    perfect_factor = perfectoid_factorization_predicate(bin_rational)
    print(f"Perfectoid factorization predicate: {perfect_factor}")


def example_perfectoid_factorization():
    """Example of perfectoid factorization analysis."""
    print("\n=== Perfectoid Factorization Analysis ===")
    
    # Test various binary p-adic patterns for perfectoid factorization
    test_patterns = [
        [1, 0, 0, 0],  # Single 1 (base case, always factors)
        [0, 1, 0, 0],  # Single 1 in different position
        [1, 1, 0, 0],  # Two adjacent 1's
        [1, 0, 1, 0],  # Two 1's with gap
        [1, 0, 0, 1],  # Two 1's with larger gap
        [1, 1, 1, 0],  # Three 1's
        [1, 0, 1, 1],  # Three 1's in different pattern
        [1, 1, 1, 1],  # Four 1's (complex pattern)
    ]
    
    print("Binary Pattern | Admits Perfectoid Factorization")
    print("-------------------------------------------")
    
    for pattern in test_patterns:
        bin_padic = BinaryPAdicNumber(pattern, prime=5)
        can_factor = perfectoid_factorization_predicate(bin_padic)
        pattern_str = ''.join(str(d) for d in pattern)
        print(f"{pattern_str.ljust(15)} | {str(can_factor)}")
    
    # Test the key factorization theorem on critical examples
    print("\nTesting Perfectoid Factorization on Critical Examples:")
    
    elements = [
        {"name": "p (prime)", "rational": (5, 1)},
        {"name": "x (variable)", "rational": (1, 1)},
        {"name": "x + p", "binary": [1, 1, 0, 0]},
        {"name": "x·p", "binary": [0, 0, 1, 0]}
    ]
    
    for elem in elements:
        if "rational" in elem:
            num, den = elem["rational"]
            bin_padic = rational_to_binary_padic(num, den, prime=5)
        else:
            bin_padic = BinaryPAdicNumber(elem["binary"], prime=5)
            
        can_factor = perfectoid_factorization_predicate(bin_padic)
        print(f"  {elem['name']}: Binary pattern = {bin_padic.binary_digits}, Factors = {can_factor}")


def example_subadditivity_counterexamples():
    """Example of testing subadditivity counterexamples."""
    print("\n=== Subadditivity Counterexample Analysis ===")
    
    # Test whether the theory resolves apparent counterexamples to subadditivity
    results = test_subadditivity_counterexamples(coefficient=0.5, prime=5)
    
    print(f"All counterexamples resolved: {results['all_counterexamples_resolved']}")
    print("\nCounterexample Details:")
    
    for detail in results["counterexample_details"]:
        print(f"\n  {detail['name']}:")
        print(f"    Elements: {detail['elements']}")
        print(f"    All elements admit factorization: {detail['all_admit_factorization']}")
        print(f"    All elements in test ideal: {detail['all_in_ideal']}")
        print(f"    Sum in test ideal: {detail['sum_in_ideal']}")
        print(f"    Subadditivity holds: {detail['subadditivity_holds']}")
        print(f"    Theory resolves this case: {detail['theory_resolves']}")
    
    # Also verify basic properties of the binary predicate
    print("\nVerifying Binary Predicate Properties:")
    prop_results = verify_binary_predicate_properties()
    
    print(f"All properties verified: {prop_results['properties_verified']}")
    for detail in prop_results["property_details"]:
        print(f"  {detail['property']} - {detail['test_case']}: {detail['satisfied']}")


def example_test_ideal_comparison():
    """Example of comparing test ideals with different coefficients."""
    print("\n=== Test Ideal Comparison ===")
    
    # Generate test cases
    test_cases = generate_test_cases(prime=5, max_num=5)
    print(f"Generated {len(test_cases)} test cases")
    
    # Display sample test cases
    print("Sample test cases:")
    for tc in test_cases[:5]:
        print(f"  {tc[0]}/{tc[1]}")
    
    # Compare test ideals with different coefficients
    comparison = compare_test_ideals(0.3, 0.7, test_cases[:5])
    
    print(f"\nComparing test ideals with coefficients 0.3 and 0.7:")
    print(f"Elements in both test ideals: {comparison['in_both']}")
    print(f"Elements only in first test ideal: {comparison['only_in_first']}")
    print(f"Elements only in second test ideal: {comparison['only_in_second']}")
    print(f"Elements in neither test ideal: {comparison['in_neither']}")
    print(f"Test ideals are equal: {comparison['equal']}")
    print(f"First contains second: {comparison['first_contains_second']}")
    print(f"Second contains first: {comparison['second_contains_first']}")
    
    print("\nDetail for each element:")
    for detail in comparison["element_details"]:
        element = detail["element"]
        if isinstance(element, tuple):
            element_str = f"{element[0]}/{element[1]}"
        else:
            element_str = str(element)
        print(f"  {element_str}: {detail['category']}")


def example_verification():
    """Example of running the verification framework."""
    print("\n=== Verification Analysis ===")
    
    # Create a verifier
    verifier = BinaryPAdicVerifier(prime=5)
    
    # Run individual verification steps
    print("Running individual verification steps...")
    global_result = verifier.verify_global_consistency()
    schema_result = verifier.verify_schema_theoretic_properties()
    perfectoid_result = verifier.verify_perfectoid_factorization()
    edge_result = verifier.verify_edge_cases()
    final_result = verifier.verify_final_consistency()
    
    # Display results
    print(f"Global consistency verified: {global_result['global_consistency']}")
    print(f"Schema properties verified: {schema_result['schema_properties_verified']}")
    print(f"Perfectoid factorization verified: {perfectoid_result['perfectoid_factorization_verified']}")
    print(f"Edge cases verified: {edge_result['edge_cases_verified']}")
    print(f"Final verification: {final_result['final_verification']}")
    
    print("\nVerification framework status:")
    for problem in verifier.verification_framework:
        print(f"\n=== {problem.problem} Verification ===")
        for component in problem.components:
            print(f"  {component.aspect}: {component.verified}")


def main():
    """Run all examples."""
    print("PAdicMath Library Examples")
    print("=========================")
    
    # Run examples
    example_padic_basics()
    example_binary_padic()
    example_perfectoid_factorization()
    example_subadditivity_counterexamples()
    example_test_ideal_comparison()
    example_verification()
    
    print("\nExamples complete!")


if __name__ == "__main__":
    main() 