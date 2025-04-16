#!/usr/bin/env python
"""
Helper script to insert visualization references into the paper sections.
This script will search for appropriate places in the paper sections to include
the generated visualizations.
"""

import os
import re
import shutil
from pathlib import Path

# Define the visualizations to insert into specific sections
SECTION_VISUALIZATIONS = {
    "binary_framework.tex": [
        {
            "visualization": "padic_digits_base_2.pdf",
            "caption": "Binary representation of $p$-adic digits for integers from $0$ to $20$. "
            + "Each row represents an integer, and columns show the binary digits $a_i$ "
            + "in the $p$-adic expansion. These digit patterns form the foundation of our test ideal theory.",
            "search_pattern": r"\\subsection{Binary Representation",
        },
        {
            "visualization": "predicate_evaluation_p2.pdf",
            "caption": "Visualization of predicate evaluation $\\mathcal{P}_\\Delta$ for test ideal membership. "
            + "The top panel shows the $p$-adic valuation compared to threshold $t_\\Delta$. "
            + "The bottom left panel shows the weighted sum component, and the right panel shows the final evaluation result.",
            "search_pattern": r"\\subsection{Predicate Construction",
        },
    ],
    "subadditivity.tex": [
        {
            "visualization": "subadditivity.pdf",
            "caption": "Illustration of the subadditivity property for test ideals, showing that "
            + "$\\tau_+(R,\\Delta_1+\\Delta_2) \\subseteq \\tau_+(R,\\Delta_1) \\cdot \\tau_+(R,\\Delta_2)$. "
            + "The property is proved via a constructive factorization approach based on the predicate decomposition.",
            "search_pattern": r"\\section{Subadditivity",
        }
    ],
    "completion_theorem.tex": [
        {
            "visualization": "completion_theorem.pdf",
            "caption": "Visualization of the completion theorem, demonstrating that test ideals commute with completion: "
            + "$\\tau_+(\\hat{R},\\hat{\\Delta}) \\cap R = \\tau_+(R,\\Delta)$. "
            + "The key insight is that predicate evaluation remains invariant for elements in the original ring $R$.",
            "search_pattern": r"\\section{Test Ideals Commute with Completion",
        }
    ],
    "alternative_formulations.tex": [
        {
            "visualization": "alternative_formulations.pdf",
            "caption": "Unification of alternative formulations of test ideals through explicit predicate modifications. "
            + "Each approach corresponds to specific transformations of the predicate components, "
            + "showing that the binary $p$-adic framework provides a unified mathematical foundation.",
            "search_pattern": r"\\section{Unification of Alternative",
        }
    ],
    "computational_algorithms.tex": [
        {
            "visualization": "computational_framework.pdf",
            "caption": "The computational framework for test ideals in mixed characteristic, showing the pipeline "
            + "from divisor input to test ideal computation. This framework makes the theory computationally "
            + "effective and applicable to concrete algebraic geometry problems.",
            "search_pattern": r"\\section{Computational",
        }
    ],
}


def backup_file(file_path):
    """Create a backup of the original file."""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    return backup_path


def insert_visualization(section_path, vis_info):
    """Insert a visualization reference at the appropriate location in a section file."""
    # Check if file exists
    if not os.path.exists(section_path):
        print(f"Error: {section_path} not found.")
        return False

    # Create a backup
    backup_file(section_path)

    # Read the current content
    with open(section_path, "r") as f:
        content = f.read()

    # Find the insertion point
    pattern = vis_info["search_pattern"]
    match = re.search(pattern, content)

    if not match:
        print(f"Could not find insertion point using pattern: {pattern}")
        return False

    # Find the end of the paragraph or the section beginning
    end_pos = match.end()
    next_empty_line = content.find("\n\n", end_pos)

    if next_empty_line == -1:
        next_empty_line = len(content)

    # Create the visualization command
    vis_command = (
        "\n\n\\includeVisualization{"
        + vis_info["visualization"]
        + "}{"
        + vis_info["caption"]
        + "}\n"
    )

    # Insert the visualization command
    new_content = content[:next_empty_line] + vis_command + content[next_empty_line:]

    # Write the modified content back
    with open(section_path, "w") as f:
        f.write(new_content)

    print(f"Inserted visualization {vis_info['visualization']} into {section_path}")
    return True


def main():
    """Insert visualizations into the paper sections."""
    sections_dir = Path("sections")

    if not sections_dir.exists():
        print("Error: 'sections' directory not found.")
        return

    # Ensure the LaTeX inclusion file is in the right place
    latex_inclusion_src = Path("visualizations/latex_inclusion.tex")
    latex_inclusion_dest = sections_dir / "latex_inclusion.tex"

    if latex_inclusion_src.exists() and not latex_inclusion_dest.exists():
        shutil.copy2(latex_inclusion_src, latex_inclusion_dest)
        print(f"Copied {latex_inclusion_src} to {latex_inclusion_dest}")

    # Process each section
    for section_file, visualizations in SECTION_VISUALIZATIONS.items():
        section_path = sections_dir / section_file

        if not section_path.exists():
            print(f"Warning: Section file {section_file} not found. Skipping.")
            continue

        print(f"\nProcessing section: {section_file}")
        for vis_info in visualizations:
            insert_visualization(section_path, vis_info)

    print("\nFinished inserting visualizations.")
    print("Please review the changes and make adjustments if needed.")
    print("You may need to update the preamble to include:")
    print("\\input{sections/latex_inclusion}")


if __name__ == "__main__":
    main()
