"""
P-adic Mathematics Library

A Python library for working with p-adic numbers and the binary p-adic test ideal theory.
This library provides tools for mathematical research on p-adic numbers and test ideals.
"""

__version__ = "0.1.0"

# Core classes
from .core.padic import PAdicNumber, BinaryPAdicNumber

# Verification tools
from .verification.verifier import (
    BinaryPAdicVerifier,
    VerificationComponent,
    VerificationProblem
)

# Utility functions
from .utils.helpers import (
    rational_to_padic,
    rational_to_binary_padic,
    padic_valuation,
    is_in_test_ideal,
    compare_test_ideals,
    generate_test_cases,
    perfectoid_factorization_predicate,
    test_subadditivity_counterexamples,
    verify_binary_predicate_properties
)

# Expose key functionality at the top level
__all__ = [
    # Core classes
    "PAdicNumber",
    "BinaryPAdicNumber",
    
    # Verification
    "BinaryPAdicVerifier",
    "VerificationComponent",
    "VerificationProblem",
    
    # Utility functions
    "rational_to_padic",
    "rational_to_binary_padic",
    "padic_valuation",
    "is_in_test_ideal",
    "compare_test_ideals",
    "generate_test_cases",
    
    # Mathematical testing functions
    "perfectoid_factorization_predicate",
    "test_subadditivity_counterexamples",
    "verify_binary_predicate_properties"
]
