"""
Binary P-adic Theory of Test Ideals - Python Implementation

This library provides computational tools for working with test ideals in mixed characteristic
based on the binary p-adic framework developed in "Binary P-adic Theory of Test Ideals
in Mixed Characteristic".
"""

from .binary import BinaryPredicate, test_ideal_membership
from .binary import subadditivity_factorization
from .binary import FormulationClassifier
from .padic import PadicElement, Divisor, QDivisor

__version__ = "0.1.0"
