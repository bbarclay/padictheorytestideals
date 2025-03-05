"""
Setup script for the padicmath package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="padicmath",
    version="0.1.0",
    author="Mathematical Research Team",
    author_email="research@example.com",
    description="A library for p-adic numbers and test ideal theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/padicmath",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
) 