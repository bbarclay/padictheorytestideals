# PAdicMath

A Python library for working with p-adic numbers and the binary p-adic test ideal theory. This mathematically rigorous package provides tools for researchers in algebraic geometry, number theory, and related fields.

## Features

- Comprehensive p-adic number representation and operations
- Binary p-adic approach to test ideals
- Verification framework for mathematical consistency
- Tools for investigating perfectoid factorization
- Utilities for test ideal comparisons and analysis

## Installation

```bash
pip install padicmath
```

Or for development:

```bash
git clone https://github.com/example/padicmath.git
cd padicmath
pip install -e .
```

## Quick Start

```python
from padicmath import PAdicNumber, BinaryPAdicNumber, rational_to_binary_padic

# Create a p-adic number
p_adic = PAdicNumber([1, 0, 1, 0, 0], prime=5)
print(p_adic)  # 1010 (base 5) × 5^0

# Convert a rational number to its p-adic representation
p_adic_rational = PAdicNumber.from_rational(7, 3, prime=5, precision=10)
print(p_adic_rational)

# Create a binary p-adic number
binary_p_adic = BinaryPAdicNumber([1, 0, 1, 0, 0], prime=5)
print(binary_p_adic)  # 10100 (binary p-adic, base 5) × 5^0

# Check if an element is in a test ideal
coefficient = 0.7  # Divisor coefficient
is_member = binary_p_adic.is_test_ideal_member(coefficient)
print(f"Element in test ideal with coefficient {coefficient}: {is_member}")

# Convert directly from rational to binary p-adic
bin_padic_rational = rational_to_binary_padic(7, 3, prime=5)
print(bin_padic_rational)
```

## Verification Framework

The library includes a comprehensive verification framework for validating the mathematical soundness of the binary p-adic approach:

```python
from padicmath import BinaryPAdicVerifier

# Create a verifier with prime p=5
verifier = BinaryPAdicVerifier(prime=5)

# Run the comprehensive verification
results = verifier.run_deep_verification_analysis()

# Access verification results
print(f"Verification successful: {results['final_verification']}")
```

## Mathematical Background

The binary p-adic test ideal theory addressed in this library focuses on three key mathematical problems:

1. **The Completion Problem**: Understanding the behavior of test ideals under completion
2. **The Subadditivity Problem**: Resolving apparent counterexamples to subadditivity using perfectoid factorization
3. **The Alternative Formulations Problem**: Characterizing the differences between various definitions of test ideals

The library implements a binary p-adic approach that provides a unified framework for these problems.

## Components

The package is organized into three main modules:

- **Core**: Basic p-adic number representation and operations
- **Verification**: Validation of the mathematical properties of the theory
- **Utils**: Helper functions for working with p-adic numbers and test ideals

## Development and Testing

```bash
# Run tests
python -m unittest discover

# Run a specific test
python -m unittest padicmath.tests.test_padic
```

## Citation

If you use this library in your research, please cite:

```
@software{padicmath,
  author = {Mathematical Research Team},
  title = {PAdicMath: A Python Library for P-adic Mathematics},
  year = {2023},
  url = {https://github.com/example/padicmath}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 