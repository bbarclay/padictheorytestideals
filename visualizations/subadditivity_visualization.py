"""
Visualization script for the subadditivity property and completion theorem.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from matplotlib_venn import venn2, venn3

# Import the common matplotlib configuration
from visualizations.matplotlib_config import configure_matplotlib

# Apply the configuration
configure_matplotlib()


def visualize_subadditivity(filename="subadditivity"):
    """
    Visualize the subadditivity property:
    τ₊(R,Δ₁+Δ₂) ⊆ τ₊(R,Δ₁) · τ₊(R,Δ₂)
    """
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(12, 10))

    # First subplot: Venn diagram representation
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    ax1.set_title("Set-Theoretic Representation of Subadditivity", fontsize=16, pad=20)

    # Create Venn diagram
    v = venn2(
        subsets=(0.6, 0.7, 0.4),
        set_labels=(r"$\tau_+(R,\Delta_1)$", r"$\tau_+(R,\Delta_2)$"),
        ax=ax1,
    )

    # Customize colors and alpha
    v.get_patch_by_id("10").set_color("#1f77b4")
    v.get_patch_by_id("01").set_color("#ff7f0e")
    v.get_patch_by_id("11").set_color("#2ca02c")

    v.get_patch_by_id("10").set_alpha(0.7)
    v.get_patch_by_id("01").set_alpha(0.7)
    v.get_patch_by_id("11").set_alpha(0.7)

    # Add another smaller set representing τ₊(R,Δ₁+Δ₂)
    center = v.get_label_by_id("11").get_position()
    subadditivity_set = Circle(center, 0.15, color="red", alpha=0.7)
    ax1.add_patch(subadditivity_set)
    ax1.text(
        center[0],
        center[1],
        r"$\tau_+(R,\Delta_1+\Delta_2)$",
        ha="center",
        va="center",
        fontsize=10,
        color="white",
    )

    # Add explanation
    ax1.text(
        0.5,
        -0.1,
        r"Subadditivity Property: $\tau_+(R,\Delta_1+\Delta_2) \subseteq \tau_+(R,\Delta_1) \cdot \tau_+(R,\Delta_2)$",
        ha="center",
        va="center",
        transform=ax1.transAxes,
        fontsize=12,
    )

    ax1.axis("off")

    # Second subplot: Algebraic representation with predicate conditions
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax2.set_title("Predicate-Based Representation", fontsize=14, pad=15)
    ax2.axis("off")

    # Create text boxes for the predicates
    predicate_text1 = (
        r"$\mathcal{P}_{\Delta_1}(\mathrm{bin}_p(x))$:" + "\n"
        r"$\mathrm{val}_p(x) < t_{\Delta_1}$ $\wedge$" + "\n"
        r"$\sum_{i=0}^{\infty} w_i(\Delta_1) \cdot \phi(a_i) < C_{\Delta_1}$"
    )

    predicate_text2 = (
        r"$\mathcal{P}_{\Delta_2}(\mathrm{bin}_p(x))$:" + "\n"
        r"$\mathrm{val}_p(x) < t_{\Delta_2}$ $\wedge$" + "\n"
        r"$\sum_{i=0}^{\infty} w_i(\Delta_2) \cdot \phi(a_i) < C_{\Delta_2}$"
    )

    predicate_text_combined = (
        r"$\mathcal{P}_{\Delta_1+\Delta_2}(\mathrm{bin}_p(x))$:" + "\n"
        r"$\mathrm{val}_p(x) < \min(t_{\Delta_1}, t_{\Delta_2})$ $\wedge$" + "\n"
        r"$\sum_{i=0}^{\infty} (w_i(\Delta_1) + w_i(\Delta_2)) \cdot \phi(a_i) < C_{\Delta_1} + C_{\Delta_2}$"
    )

    # Create background boxes with some padding
    bbox_props = dict(boxstyle="round,pad=0.5", fc="#f0f0f0", ec="black", lw=1)

    # Position the text boxes
    ax2.text(
        0.25,
        0.75,
        predicate_text1,
        ha="center",
        va="center",
        bbox=bbox_props,
        fontsize=10,
    )
    ax2.text(
        0.75,
        0.75,
        predicate_text2,
        ha="center",
        va="center",
        bbox=bbox_props,
        fontsize=10,
    )
    ax2.text(
        0.5,
        0.25,
        predicate_text_combined,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="#ffe6e6", ec="red", lw=1),
        fontsize=10,
    )

    # Add arrows to show relationship
    arrow1 = FancyArrowPatch(
        (0.25, 0.6),
        (0.4, 0.4),
        arrowstyle="->",
        mutation_scale=20,
        color="blue",
        linewidth=1.5,
        connectionstyle="arc3,rad=0.2",
    )
    arrow2 = FancyArrowPatch(
        (0.75, 0.6),
        (0.6, 0.4),
        arrowstyle="->",
        mutation_scale=20,
        color="orange",
        linewidth=1.5,
        connectionstyle="arc3,rad=-0.2",
    )
    ax2.add_patch(arrow1)
    ax2.add_patch(arrow2)

    # Third subplot: Factorization approach visualization
    ax3 = plt.subplot2grid((2, 2), (1, 1))
    ax3.set_title("Constructive Factorization Approach", fontsize=14, pad=15)
    ax3.axis("off")

    # Create boxes for elements and factorization
    x_box = Rectangle((0.1, 0.7), 0.8, 0.2, fc="#e6f2ff", ec="black", lw=1)
    factorization_box = Rectangle((0.1, 0.3), 0.8, 0.2, fc="#e6ffe6", ec="black", lw=1)

    ax3.add_patch(x_box)
    ax3.add_patch(factorization_box)

    # Add text to the boxes
    ax3.text(
        0.5,
        0.8,
        r"$x \in \tau_+(R,\Delta_1+\Delta_2)$",
        ha="center",
        va="center",
        fontsize=12,
    )
    ax3.text(
        0.5,
        0.4,
        r"$x = y \cdot z$ where $y \in \tau_+(R,\Delta_1)$ and $z \in \tau_+(R,\Delta_2)$",
        ha="center",
        va="center",
        fontsize=12,
    )

    # Add arrow to show the factorization
    main_arrow = FancyArrowPatch(
        (0.5, 0.7),
        (0.5, 0.5),
        arrowstyle="->",
        mutation_scale=20,
        color="green",
        linewidth=2,
    )
    ax3.add_patch(main_arrow)

    # Add explanation at the bottom
    ax3.text(
        0.5,
        0.1,
        "The subadditivity property is proved by constructively factorizing\n"
        r"elements of $\tau_+(R,\Delta_1+\Delta_2)$ into products from the individual ideals.",
        ha="center",
        va="center",
        fontsize=10,
    )

    # Add descriptive caption at the bottom of the figure
    caption = (
        "Figure: Visualization of the subadditivity property for test ideals. "
        "The top panel shows a set-theoretic representation. "
        "The bottom left panel illustrates the predicate-based characterization. "
        "The bottom right panel demonstrates the constructive factorization approach used in the proof."
    )
    plt.figtext(0.5, 0.01, caption, ha="center", fontsize=9, wrap=True)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Save the figure with high resolution
    plt.savefig(f"visualizations/output/{filename}.pdf", bbox_inches="tight")
    plt.savefig(f"visualizations/output/{filename}.png", bbox_inches="tight")
    plt.close()

    print(f"Generated {filename}.pdf and {filename}.png in visualizations/output/")


def visualize_completion_theorem(filename="completion_theorem"):
    """
    Visualize the completion theorem:
    τ₊(R̂,Δ̂) ∩ R = τ₊(R,Δ)
    """
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Left subplot: Venn diagram representation
    ax1.set_title(
        "Set-Theoretic Representation of Completion Theorem", fontsize=16, pad=20
    )

    # Draw the outer ring representing R̂ (completion of R)
    outer_circle = plt.Circle(
        (0.5, 0.5), 0.4, fill=False, edgecolor="black", linewidth=2
    )
    ax1.add_patch(outer_circle)
    ax1.text(
        0.5, 0.95, r"$\hat{R}$ (Completion)", ha="center", va="center", fontsize=12
    )

    # Draw the inner circle representing R
    inner_circle = plt.Circle(
        (0.5, 0.5),
        0.25,
        fill=True,
        color="#e6f2ff",
        alpha=0.5,
        edgecolor="blue",
        linewidth=2,
    )
    ax1.add_patch(inner_circle)
    ax1.text(0.5, 0.5, r"$R$ (Original Ring)", ha="center", va="center", fontsize=10)

    # Draw the test ideal in the completion
    test_ideal_hat = plt.Circle(
        (0.6, 0.6),
        0.2,
        fill=True,
        color="#ffe6e6",
        alpha=0.6,
        edgecolor="red",
        linewidth=1.5,
    )
    ax1.add_patch(test_ideal_hat)
    ax1.text(
        0.7,
        0.7,
        r"$\tau_+(\hat{R},\hat{\Delta})$",
        ha="center",
        va="center",
        fontsize=10,
    )

    # Draw the intersection and the original test ideal
    # They are the same according to the theorem
    intersection = plt.Circle(
        (0.54, 0.54),
        0.12,
        fill=True,
        color="#e6ffe6",
        alpha=0.7,
        edgecolor="green",
        linewidth=1.5,
    )
    ax1.add_patch(intersection)
    ax1.text(0.54, 0.54, r"$\tau_+(R,\Delta)$", ha="center", va="center", fontsize=8)

    # Add explanation
    ax1.text(
        0.5,
        0.1,
        r"Completion Theorem: $\tau_+(\hat{R},\hat{\Delta}) \cap R = \tau_+(R,\Delta)$",
        ha="center",
        va="center",
        fontsize=12,
    )

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis("off")

    # Right subplot: Algebraic representation with predicate conditions
    ax2.set_title("Predicate Invariance Under Completion", fontsize=16, pad=20)
    ax2.axis("off")

    # Create text boxes for the original and completed predicates
    predicate_text_original = (
        r"Predicate in $R$:" + "\n"
        r"$\mathcal{P}_{\Delta}(\mathrm{bin}_p(x))$:" + "\n"
        r"$\mathrm{val}_p(x) < t_{\Delta}$ $\wedge$" + "\n"
        r"$\sum_{i=0}^{\infty} w_i(\Delta) \cdot \phi(a_i) < C_{\Delta}$"
    )

    predicate_text_completion = (
        r"Predicate in $\hat{R}$:" + "\n"
        r"$\mathcal{P}_{\hat{\Delta}}(\mathrm{bin}_p(x))$:" + "\n"
        r"$\mathrm{val}_p(x) < t_{\hat{\Delta}}$ $\wedge$" + "\n"
        r"$\sum_{i=0}^{\infty} w_i(\hat{\Delta}) \cdot \phi(a_i) < C_{\hat{\Delta}}$"
    )

    invariance_text = (
        r"Key Insight:" + "\n"
        r"For $x \in R$, the predicate evaluation" + "\n"
        r"is identical in both $R$ and $\hat{R}$" + "\n"
        r"since the $p$-adic digit representation" + "\n"
        r"and the parameters $t_{\Delta}$, $w_i(\Delta)$," + "\n"
        r"and $C_{\Delta}$ remain unchanged under completion."
    )

    # Create background boxes with some padding
    bbox_props = dict(boxstyle="round,pad=0.5", fc="#f0f0f0", ec="black", lw=1)

    # Position the text boxes
    ax2.text(
        0.25,
        0.7,
        predicate_text_original,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="#e6f2ff", ec="blue", lw=1),
        fontsize=10,
    )
    ax2.text(
        0.75,
        0.7,
        predicate_text_completion,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="#ffe6e6", ec="red", lw=1),
        fontsize=10,
    )
    ax2.text(
        0.5,
        0.25,
        invariance_text,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="#e6ffe6", ec="green", lw=1),
        fontsize=10,
    )

    # Add double-headed arrow to show equivalence for elements in R
    arrow = FancyArrowPatch(
        (0.35, 0.7),
        (0.65, 0.7),
        arrowstyle="<->",
        mutation_scale=20,
        color="black",
        linewidth=1.5,
        connectionstyle="arc3,rad=0.2",
    )
    ax2.add_patch(arrow)
    ax2.text(
        0.5, 0.8, r"Equivalent for $x \in R$", ha="center", va="center", fontsize=10
    )

    # Add arrows pointing to the invariance box
    arrow1 = FancyArrowPatch(
        (0.25, 0.55),
        (0.4, 0.35),
        arrowstyle="->",
        mutation_scale=15,
        color="blue",
        linewidth=1,
        connectionstyle="arc3,rad=-0.2",
    )
    arrow2 = FancyArrowPatch(
        (0.75, 0.55),
        (0.6, 0.35),
        arrowstyle="->",
        mutation_scale=15,
        color="red",
        linewidth=1,
        connectionstyle="arc3,rad=0.2",
    )
    ax2.add_patch(arrow1)
    ax2.add_patch(arrow2)

    # Add descriptive caption at the bottom of the figure
    caption = (
        "Figure: Visualization of the completion theorem for test ideals. "
        "The left panel shows the set-theoretic relationship between the original ring, its completion, and the corresponding test ideals. "
        "The right panel illustrates why the predicate-based characterization remains invariant for elements of the original ring $R$."
    )
    plt.figtext(0.5, 0.01, caption, ha="center", fontsize=9, wrap=True)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Save the figure with high resolution
    plt.savefig(f"visualizations/output/{filename}.pdf", bbox_inches="tight")
    plt.savefig(f"visualizations/output/{filename}.png", bbox_inches="tight")
    plt.close()

    print(f"Generated {filename}.pdf and {filename}.png in visualizations/output/")


if __name__ == "__main__":
    # Generate the visualizations
    visualize_subadditivity()
    visualize_completion_theorem()

    print("All theorem visualizations completed.")
