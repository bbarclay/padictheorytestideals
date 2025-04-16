"""
Visualization script for alternative formulations and computational framework.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import FancyArrowPatch, Rectangle

# Import the common matplotlib configuration
from visualizations.matplotlib_config import configure_matplotlib

# Apply the configuration
configure_matplotlib()


def visualize_alternative_formulations(filename="alternative_formulations"):
    """
    Visualize the unification of alternative formulations of test ideals
    through explicit predicate modifications.
    """
    # Create a figure
    fig = plt.figure(figsize=(12, 9))

    # Set up a central "Binary p-adic Framework" box
    ax = plt.subplot2grid((1, 1), (0, 0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Create the central box
    central_box = Rectangle((4, 4.5), 2, 1, fc="#2171b5", ec="black", lw=2, alpha=0.7)
    ax.add_patch(central_box)
    ax.text(
        5,
        5.2,
        r"Binary $p$-adic",
        ha="center",
        va="center",
        color="white",
        fontsize=14,
        fontweight="bold",
    )
    ax.text(
        5,
        4.8,
        r"Framework",
        ha="center",
        va="center",
        color="white",
        fontsize=14,
        fontweight="bold",
    )

    # Create boxes for alternative formulations
    formulations = [
        ("Perfectoid Approach", 2, 7.5, "#66c2a5"),
        ("Cartier Algebras", 5, 8.5, "#fc8d62"),
        ("Big Cohen-Macaulay Algebras", 8, 7.5, "#8da0cb"),
        (r"Faltings\' Almost Mathematics", 2, 2.5, "#e78ac3"),
        (r"Regular $p$-adic Hodge Theory", 5, 1.5, "#a6d854"),
        ("Non-standard Frobenius", 8, 2.5, "#ffd92f"),
    ]

    boxes = []
    for name, x, y, color in formulations:
        box = Rectangle(
            (x - 1.5, y - 0.5), 3, 1, fc=color, ec="black", lw=1.5, alpha=0.7
        )
        ax.add_patch(box)
        ax.text(x, y, name, ha="center", va="center", fontsize=12)
        boxes.append((name, x, y, color, box))

    # Add connecting arrows with transformation labels
    transformations = [
        (0, r"$\phi(a_i) \rightarrow \phi(a_i) \cdot \theta(i)$"),
        (1, r"$w_i(\Delta) \rightarrow w_i(\Delta) \cdot \tau(i)$"),
        (2, r"$t_\Delta \rightarrow t_\Delta + \kappa$"),
        (3, r"$C_\Delta \rightarrow C_\Delta \cdot \lambda$"),
        (4, r"$a_i \rightarrow \psi(a_i)$"),
        (5, "Combined transforms"),
    ]

    for (idx, label), (name, x, y, color, box) in zip(transformations, boxes):
        # Calculate arrow start and end points
        if y > 5:  # Top boxes
            start_x, start_y = x, y - 0.5
            end_x, end_y = 5, 5.5
            arrow = FancyArrowPatch(
                (start_x, start_y),
                (end_x, end_y),
                arrowstyle="->",
                mutation_scale=20,
                color=color,
                linewidth=2,
                connectionstyle="arc3,rad=0.3",
            )
            text_x = (start_x + end_x) / 2 + 0.5
            text_y = (start_y + end_y) / 2 + 0.3
            ax.text(
                text_x,
                text_y,
                label,
                ha="center",
                va="center",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, alpha=0.8),
            )
        else:  # Bottom boxes
            start_x, start_y = x, y + 0.5
            end_x, end_y = 5, 4.5
            arrow = FancyArrowPatch(
                (start_x, start_y),
                (end_x, end_y),
                arrowstyle="->",
                mutation_scale=20,
                color=color,
                linewidth=2,
                connectionstyle="arc3,rad=-0.3",
            )
            text_x = (start_x + end_x) / 2 + 0.5
            text_y = (start_y + end_y) / 2 - 0.3
            ax.text(
                text_x,
                text_y,
                label,
                ha="center",
                va="center",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, alpha=0.8),
            )

        ax.add_patch(arrow)

    # Add the predicate in the center of the diagram
    predicate_text = (
        r"$\mathcal{P}_\Delta(\mathrm{bin}_p(x)) = (\mathrm{val}_p(x) < t_\Delta) \wedge "
        r"(\sum_{i=0}^{\infty} w_i(\Delta) \cdot \phi(a_i) < C_\Delta)$"
    )
    ax.text(
        5,
        3.5,
        predicate_text,
        ha="center",
        va="center",
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#2171b5", lw=1.5),
    )

    # Add title
    plt.suptitle(
        "Unification of Alternative Formulations via Predicate Modifications",
        fontsize=16,
        y=0.98,
    )

    # Add descriptive caption
    caption = (
        "Figure: Visualization of how different formulations of test ideals can be unified through explicit "
        "modifications to the predicate parameters. Each approach corresponds to specific transformations of "
        "the predicate components, showing that the binary p-adic framework provides a unified mathematical foundation."
    )
    plt.figtext(0.5, 0.02, caption, ha="center", fontsize=9, wrap=True)

    # Save the figure with high resolution
    plt.savefig(f"visualizations/output/{filename}.pdf", bbox_inches="tight")
    plt.savefig(f"visualizations/output/{filename}.png", bbox_inches="tight")
    plt.close()

    print(f"Generated {filename}.pdf and {filename}.png in visualizations/output/")


def visualize_computational_framework(filename="computational_framework"):
    """
    Visualize the computational framework for mixed characteristic algebraic geometry.
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")

    # Set up the computational pipeline
    pipeline_steps = [
        ("Input", r"Divisor $\Delta$ on\nScheme $X$ over\nmixed characteristic", 0),
        ("Decomposition", r"Express $\Delta$ in terms of\n$p$-adic digit patterns", 1),
        (
            "Parameter Extraction",
            r"Compute $t_\Delta$, $w_i(\Delta)$, $C_\Delta$\nfrom $\Delta$",
            2,
        ),
        (
            "Predicate Construction",
            r"Build $\mathcal{P}_\Delta(\mathrm{bin}_p(x))$\nwith the parameters",
            3,
        ),
        (
            "Test Ideal Computation",
            r"Determine elements satisfying\nthe predicate $\mathcal{P}_\Delta$",
            4,
        ),
        ("Output", r"Test ideal $\tau_+(R,\Delta)$\nwith computational properties", 5),
    ]

    # Layout parameters
    y_pos = 6
    box_height = 1.2
    main_width = 3.5
    spacing = 0.7

    # Draw the pipeline
    for i, (title, description, level) in enumerate(pipeline_steps):
        # Box coordinates
        x_left = 1 + level * (main_width + spacing)
        y_bottom = y_pos - box_height

        # Create a box for each step
        color = plt.cm.viridis(level / (len(pipeline_steps) - 1))
        box = Rectangle(
            (x_left, y_bottom),
            main_width,
            box_height,
            fc=color,
            ec="black",
            lw=1.5,
            alpha=0.7,
        )
        ax.add_patch(box)

        # Add title and description
        ax.text(
            x_left + main_width / 2,
            y_pos - 0.3,
            title,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )

        # Split the description by newlines and add each part separately
        desc_parts = description.split(r"\n")
        for j, part in enumerate(desc_parts):
            offset = 0.6 + j * 0.4  # Adjust vertical spacing
            ax.text(
                x_left + main_width / 2,
                y_pos - offset,
                part,
                ha="center",
                va="center",
                fontsize=10,
            )

        # Add connecting arrow to the next box
        if i < len(pipeline_steps) - 1:
            next_x = x_left + main_width + spacing
            arrow = FancyArrowPatch(
                (x_left + main_width, y_pos - box_height / 2),
                (next_x, y_pos - box_height / 2),
                arrowstyle="->",
                mutation_scale=15,
                color="black",
                linewidth=1.5,
            )
            ax.add_patch(arrow)

    # Add computational advantages at the bottom
    advantages = [
        ("Explicit", "Provides explicit\ncharacterization\nof test ideals", 0),
        ("Efficient", "Enables algorithmic\ncomputations with\nfinite checks", 1),
        (
            "Unified",
            "Connects different\nformulations through\npredicate modifications",
            2,
        ),
        ("Extensible", "Generalizes to\nglobal properties\nof schemes", 3),
    ]

    # Draw the advantages section
    for i, (title, description, pos) in enumerate(advantages):
        x_pos = 2.5 + pos * 5
        y_pos = 3

        # Add title and description in a small box
        ax.text(
            x_pos,
            y_pos,
            title,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.5",
                fc=plt.cm.plasma(pos / 3),
                ec="black",
                alpha=0.7,
            ),
        )

        # Split description by newlines and add each part separately
        desc_parts = description.split("\n")
        for j, part in enumerate(desc_parts):
            offset = 0.7 + j * 0.4  # Adjust vertical spacing
            ax.text(x_pos, y_pos - offset, part, ha="center", va="center", fontsize=10)

    # Add a section for applications
    ax.text(
        3, 1.5, "Applications", ha="center", va="center", fontsize=14, fontweight="bold"
    )

    applications = [
        ("Singularity Analysis", 1.5, 0.7),
        ("Resolution of Singularities", 3, 0.7),
        ("Birational Geometry", 4.5, 0.7),
    ]

    for title, x, y in applications:
        ax.text(
            x,
            y,
            title,
            ha="center",
            va="center",
            fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", fc="#e6f5ff", ec="black"),
        )

    # Add title
    plt.suptitle(
        "Computational Framework for Mixed Characteristic Algebraic Geometry",
        fontsize=16,
        y=0.98,
    )

    # Add descriptive caption
    caption = (
        "Figure: Visualization of the computational framework for test ideals in mixed characteristic. "
        "The pipeline illustrates how the binary p-adic approach transforms a geometric divisor into "
        "explicit computational objects. The bottom sections highlight computational advantages and applications."
    )
    plt.figtext(0.5, 0.02, caption, ha="center", fontsize=9, wrap=True)

    # Save the figure with high resolution
    plt.savefig(f"visualizations/output/{filename}.pdf", bbox_inches="tight")
    plt.savefig(f"visualizations/output/{filename}.png", bbox_inches="tight")
    plt.close()

    print(f"Generated {filename}.pdf and {filename}.png in visualizations/output/")


if __name__ == "__main__":
    # Generate the visualizations
    visualize_alternative_formulations()
    visualize_computational_framework()

    print("All formulation and framework visualizations completed.")
