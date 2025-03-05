"""
Unit tests for the helper utilities in the padicmath package.
"""
import unittest
import numpy as np
from padicmath import (
    PAdicNumber,
    BinaryPAdicNumber,
    rational_to_padic, 
    rational_to_binary_padic,
    padic_valuation,
    is_in_test_ideal,
    compare_test_ideals, 
    generate_test_cases
)


class TestHelperFunctions(unittest.TestCase):
    """Test cases for the helper functions."""
    
    def test_rational_to_padic(self):
        """Test conversion from rational to p-adic number."""
        # Test simple case
        p_adic = rational_to_padic(1, 1, prime=5)
        self.assertEqual(p_adic.digits[0], 1)
        self.assertEqual(p_adic.valuation, 0)
        
        # Test rational divisible by p
        p_adic = rational_to_padic(5, 1, prime=5)
        self.assertEqual(p_adic.digits[0], 0)
        self.assertEqual(p_adic.digits[1], 1)
        self.assertEqual(p_adic.valuation, 1)
        
        # Test fraction with denominator divisible by p
        p_adic = rational_to_padic(1, 5, prime=5)
        self.assertEqual(p_adic.valuation, -1)
    
    def test_rational_to_binary_padic(self):
        """Test conversion from rational to binary p-adic number."""
        # Test simple case
        bin_padic = rational_to_binary_padic(1, 1, prime=5)
        self.assertEqual(bin_padic.binary_digits[0], 1)
        self.assertEqual(bin_padic.valuation, 0)
        
        # Test with mixed digits
        bin_padic = rational_to_binary_padic(6, 1, prime=5)
        self.assertEqual(bin_padic.digits[0], 1)
        self.assertEqual(bin_padic.digits[1], 1)
        self.assertEqual(bin_padic.binary_digits[0], 1)
        self.assertEqual(bin_padic.binary_digits[1], 1)
    
    def test_padic_valuation(self):
        """Test p-adic valuation calculation."""
        # Test basic cases
        self.assertEqual(padic_valuation(0, 5), float('inf'))
        self.assertEqual(padic_valuation(1, 5), 0)
        self.assertEqual(padic_valuation(5, 5), 1)
        self.assertEqual(padic_valuation(25, 5), 2)
        self.assertEqual(padic_valuation(125, 5), 3)
        
        # Test mixed cases
        self.assertEqual(padic_valuation(10, 5), 1)  # 10 = 2*5
        self.assertEqual(padic_valuation(15, 5), 1)  # 15 = 3*5
        self.assertEqual(padic_valuation(50, 5), 2)  # 50 = 2*5^2
    
    def test_is_in_test_ideal(self):
        """Test test ideal membership check."""
        # Test with PAdicNumber
        p_adic = PAdicNumber([1, 0, 0], prime=5)
        self.assertTrue(is_in_test_ideal(p_adic, 0.5))
        
        # Test with BinaryPAdicNumber
        bin_padic = BinaryPAdicNumber([0, 1, 0], prime=5)
        self.assertTrue(is_in_test_ideal(bin_padic, 0.5))
        self.assertFalse(is_in_test_ideal(bin_padic, 0.2))
        
        # Test with rational tuple
        self.assertTrue(is_in_test_ideal((1, 1), 0.5, prime=5))
        self.assertTrue(is_in_test_ideal((5, 1), 0.5, prime=5))
        
        # Test with invalid type - modified to use try/except instead of with statement
        try:
            is_in_test_ideal("not a valid input", 0.5)
            self.fail("Expected TypeError but no exception was raised")
        except TypeError:
            pass  # This is the expected behavior
    
    def test_compare_test_ideals(self):
        """Test comparison of test ideals with different coefficients."""
        # Create some test elements
        test_elements = [
            (1, 1),      # 1
            (2, 1),      # 2
            (5, 1),      # 5
            (1, 5),      # 1/5
            (7, 3)       # 7/3
        ]
        
        # Compare test ideals with coefficients 0.3 and 0.7
        result = compare_test_ideals(0.3, 0.7, test_elements)
        
        # Check general structure
        self.assertIn("in_both", result)
        self.assertIn("only_in_first", result)
        self.assertIn("only_in_second", result)
        self.assertIn("in_neither", result)
        self.assertEqual(len(result["element_details"]), 5)
        
        # Check counts
        self.assertGreaterEqual(result["in_both"], 0)
        self.assertGreaterEqual(result["only_in_first"], 0)
        self.assertGreaterEqual(result["only_in_second"], 0)
        self.assertGreaterEqual(result["in_neither"], 0)
        
        # Check relations
        self.assertIn("equal", result)
        self.assertIn("first_contains_second", result)
        self.assertIn("second_contains_first", result)
        
        # Test with invalid coefficients
        with self.assertRaises(ValueError):
            compare_test_ideals(0, 0.5, test_elements)
        with self.assertRaises(ValueError):
            compare_test_ideals(0.5, 1, test_elements)
    
    def test_generate_test_cases(self):
        """Test generation of test cases."""
        # Generate only integers
        test_cases = generate_test_cases(prime=5, max_num=3, include_fractions=False)
        
        # Should include -3, -2, -1, 1, 2, 3 (all as tuples with denominator 1)
        self.assertEqual(len(test_cases), 6)
        self.assertIn((-3, 1), test_cases)
        self.assertIn((-2, 1), test_cases)
        self.assertIn((-1, 1), test_cases)
        self.assertIn((1, 1), test_cases)
        self.assertIn((2, 1), test_cases)
        self.assertIn((3, 1), test_cases)
        
        # Generate with fractions
        test_cases = generate_test_cases(prime=5, max_num=2, include_fractions=True)
        
        # Should include integers -2, -1, 1, 2 and fractions with coprime denominators
        self.assertGreater(len(test_cases), 4)  # At least the integers
        self.assertIn((-2, 1), test_cases)
        self.assertIn((-1, 1), test_cases)
        self.assertIn((1, 1), test_cases)
        self.assertIn((2, 1), test_cases)
        
        # Check some fractions
        self.assertIn((1, 2), test_cases)
        self.assertIn((2, 1), test_cases)
        
        # Check that fractions are in reduced form
        for num, den in test_cases:
            if den > 1:
                self.assertEqual(np.gcd(abs(num), den), 1)


if __name__ == '__main__':
    unittest.main() 