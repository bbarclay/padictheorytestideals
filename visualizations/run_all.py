#!/usr/bin/env python
"""
Run all visualizations for the p-adic test ideals project.
This script will generate all visualizations and save them to the output directory.
"""

import os
import sys
import traceback
import matplotlib.pyplot as plt

# Import the common matplotlib configuration
from visualizations.matplotlib_config import configure_matplotlib


def main():
    """Run all visualization scripts."""
    # Ensure the output directory exists and configure matplotlib
    os.makedirs("visualizations/output", exist_ok=True)
    configure_matplotlib()

    # Run each visualization individually
    print("Generating p-adic digit pattern visualizations...")
    try:
        from visualizations.padic_digits import visualize_padic_digits

        for p in [2, 3, 5]:
            visualize_padic_digits(p=p, filename=f"padic_digits_base_{p}")
        print("Successfully generated p-adic digit visualizations")
    except Exception as e:
        print(f"Error generating p-adic digit visualizations: {e}")
        traceback.print_exc()

    print("\nGenerating predicate evaluation visualizations...")
    try:
        from visualizations.predicate_visualization import (
            visualize_predicate_evaluation,
        )

        visualize_predicate_evaluation(p=2, filename="predicate_evaluation_p2")
        visualize_predicate_evaluation(p=3, filename="predicate_evaluation_p3")
        visualize_predicate_evaluation(
            p=5, t_delta=3, C_delta=0.8, filename="predicate_evaluation_p5"
        )
        print("Successfully generated predicate evaluation visualizations")
    except Exception as e:
        print(f"Error generating predicate evaluation visualizations: {e}")
        traceback.print_exc()

    print("\nGenerating subadditivity visualization...")
    try:
        from visualizations.subadditivity_visualization import (
            visualize_subadditivity,
            visualize_completion_theorem,
        )

        visualize_subadditivity()
        visualize_completion_theorem()
        print(
            "Successfully generated subadditivity and completion theorem visualizations"
        )
    except Exception as e:
        print(f"Error generating subadditivity visualizations: {e}")
        traceback.print_exc()

    print("\nGenerating alternative formulations visualizations...")
    try:
        from visualizations.alternative_formulations import (
            visualize_alternative_formulations,
            visualize_computational_framework,
        )

        visualize_alternative_formulations()
        visualize_computational_framework()
        print("Successfully generated alternative formulations visualizations")
    except Exception as e:
        print(f"Error generating alternative formulations visualizations: {e}")
        traceback.print_exc()

    # Report on generated files
    output_files = os.listdir("visualizations/output")
    print("\nVisualization generation complete!")
    print(f"All visualizations are saved in the 'visualizations/output' directory")
    print(f"Generated {len(output_files)} visualization files")

    # List the generated files
    if output_files:
        print("\nGenerated files:")
        for file in sorted(output_files):
            print(f"- {file}")


if __name__ == "__main__":
    main()
