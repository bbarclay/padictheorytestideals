"""
Common matplotlib configuration for all visualization scripts.
This ensures consistent styling and proper LaTeX rendering.
"""

import matplotlib.pyplot as plt
import os


def configure_matplotlib():
    """Configure matplotlib with proper LaTeX rendering and styling."""
    # Create output directory if it doesn't exist
    os.makedirs("visualizations/output", exist_ok=True)

    # Set up matplotlib parameters
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Computer Modern Roman"]

    # Configure LaTeX with necessary packages for math operators
    plt.rcParams["text.usetex"] = True
    plt.rcParams[
        "text.latex.preamble"
    ] = r"""
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{amsfonts}
    \usepackage{mathtools}
    """
