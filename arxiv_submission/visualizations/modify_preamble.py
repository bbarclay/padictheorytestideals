#!/usr/bin/env python
"""
Update the preamble.tex file to include visualization support.
This script reads the current preamble.tex file, adds the visualization package
requirements and input command, and writes the modified file back.
"""

import os
import re
import shutil
from pathlib import Path


def backup_file(file_path):
    """Create a backup of the original file."""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    return backup_path


def update_preamble(preamble_path):
    """Update the preamble.tex file to include visualization support."""
    # Check if file exists
    if not os.path.exists(preamble_path):
        print(f"Error: {preamble_path} not found.")
        return False

    # Create a backup
    backup_file(preamble_path)

    # Read the current content
    with open(preamble_path, "r") as f:
        content = f.read()

    # Check if graphicx is already included
    if "\\usepackage{graphicx}" not in content:
        # Add graphicx package right before the document ends or after the last package inclusion
        if "\\usepackage" in content:
            pattern = r"(\\usepackage\{[^}]*\})"
            last_package = re.findall(pattern, content)[-1]
            content = content.replace(
                last_package,
                f"{last_package}\n\n% Added for visualizations\n\\usepackage{{graphicx}}",
            )
        else:
            content += "\n\n% Added for visualizations\n\\usepackage{graphicx}\n"

    # Check if visualization commands are already included
    if "\\input{visualizations/latex_inclusion.tex}" not in content:
        # Add the visualization input command at the end
        content += "\n\n% Include visualization commands\n\\input{visualizations/latex_inclusion.tex}\n"

    # Write the modified content back
    with open(preamble_path, "w") as f:
        f.write(content)

    print(f"Updated {preamble_path} with visualization support.")
    return True


def main():
    """Update the preamble.tex file."""
    # Find the preamble.tex file
    preamble_path = Path("sections/preamble.tex")

    if not preamble_path.exists():
        print("preamble.tex not found in the expected location.")
        print("Searching for preamble.tex in the project...")
        preamble_paths = list(Path(".").glob("**/preamble.tex"))

        if not preamble_paths:
            print("Error: Could not find preamble.tex in the project.")
            return

        preamble_path = preamble_paths[0]
        print(f"Found preamble.tex at {preamble_path}")

    # Update the preamble
    update_preamble(preamble_path)

    print("\nNext steps:")
    print("1. Generate the visualizations by running: python visualizations/run_all.py")
    print(
        "2. Include visualizations in your document using the \\includeVisualization command"
    )
    print("   Example: \\includeVisualization{padic_digits_base_2.pdf}{Caption text}")


if __name__ == "__main__":
    main()
