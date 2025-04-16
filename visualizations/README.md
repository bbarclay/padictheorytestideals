# Visualizations for P-adic Test Ideals

This directory contains Python scripts for generating visualizations for the "Binary P-adic Theory of Test Ideals in Mixed Characteristic" paper.

## What's Included

- High-quality visualizations for key concepts in the paper
- Scripts to generate the visualizations
- LaTeX commands for easy inclusion in the paper
- Helper scripts to insert visualizations into the right sections

## Generated Visualizations

1. **P-adic Digit Patterns** (padic_digits_base_*.pdf)
   - Visualization of p-adic digit patterns for different prime bases

2. **Predicate Evaluation** (predicate_evaluation_*.pdf)
   - Visualization of the test ideal membership predicate evaluation

3. **Subadditivity Property** (subadditivity.pdf)
   - Illustration of the subadditivity property for test ideals

4. **Completion Theorem** (completion_theorem.pdf)
   - Visualization of the theorem that test ideals commute with completion

5. **Alternative Formulations** (alternative_formulations.pdf)
   - Diagram showing how the binary p-adic framework unifies alternative approaches

6. **Computational Framework** (computational_framework.pdf)
   - Flowchart of the computational pipeline for test ideals

## Quick Start

1. Install the required dependencies:
   ```bash
   pip install -r visualizations/requirements.txt
   ```

2. Generate all visualizations:
   ```bash
   python visualizations/run_all.py
   ```

3. Update your LaTeX preamble to include the visualization commands:
   ```bash
   python visualizations/modify_preamble.py
   ```

4. (Optional) Automatically insert visualizations into your paper sections:
   ```bash
   python visualizations/insert_visualizations.py
   ```

## Manual Inclusion

You can also manually include visualizations in your LaTeX document using the provided commands:

```latex
\includeVisualization[0.8]{padic_digits_base_2.pdf}{Caption text goes here}
```

The optional parameter (0.8) controls the width of the image as a fraction of \textwidth.

## Structure

- `*.py` - Individual visualization scripts
- `run_all.py` - Script to run all visualizations
- `requirements.txt` - Python dependencies
- `latex_inclusion.tex` - LaTeX commands for including visualizations in the paper
- `modify_preamble.py` - Script to update the preamble with visualization support
- `insert_visualizations.py` - Script to automatically insert visualizations into paper sections
- `example_usage.tex` - Example LaTeX document showing how to use the visualizations
- `output/` - Directory where generated visualizations are saved (both PDF and PNG formats)

## Requirements

The visualization scripts require Python 3.6+ and the following dependencies:
- matplotlib>=3.5.0
- numpy>=1.20.0
- matplotlib-venn>=0.11.7

Additionally, for proper LaTeX rendering in the visualizations, you need a LaTeX distribution installed on your system.

## Example Visualization

To view an example of how these visualizations look in a LaTeX document, you can compile the example_usage.tex file:

```bash
cd visualizations
cp output/* .  # Copy visualization files to the current directory
pdflatex example_usage.tex
```

## Customization

If you want to customize the visualizations, you can edit the corresponding Python scripts and regenerate the images. Each script has parameters that can be adjusted to change the appearance of the visualizations. 