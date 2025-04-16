import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import os

# Import the common matplotlib configuration
from visualizations.matplotlib_config import configure_matplotlib

# Apply the configuration
configure_matplotlib()


def visualize_padic_digits(p=3, max_digits=8, max_value=20, filename="padic_digits"):
    """
    Visualize p-adic digit patterns for values from 0 to max_value.

    Parameters:
    -----------
    p : int
        The prime base for p-adic expansion
    max_digits : int
        Maximum number of digits to display
    max_value : int
        Maximum value to compute p-adic expansions for
    filename : str
        Base filename for saving the figure
    """

    # Function to compute p-adic digits
    def padic_digits(n, p, digits):
        result = []
        for _ in range(digits):
            result.append(n % p)
            n //= p
        return result

    # Compute p-adic expansions for numbers 0 to max_value
    expansions = [padic_digits(n, p, max_digits) for n in range(max_value + 1)]

    # Create a visually appealing color map
    cmap = plt.cm.viridis
    norm = mcolors.Normalize(vmin=0, vmax=p - 1)

    # Set up the figure with adequate spacing
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)

    # Create the visualization
    for i, expansion in enumerate(expansions):
        for j, digit in enumerate(expansion):
            color = cmap(norm(digit))
            rect = Rectangle((j, i), 0.8, 0.8, color=color, ec="white", lw=1)
            ax.add_patch(rect)
            # Add text with the digit value
            ax.text(
                j + 0.4,
                i + 0.4,
                str(digit),
                ha="center",
                va="center",
                color="white" if digit > p // 2 else "black",
                fontsize=9,
            )

    # Set axes limits
    ax.set_xlim(-0.2, max_digits)
    ax.set_ylim(-0.2, max_value + 0.8)

    # Add labels and title with ample spacing
    ax.set_xlabel(r"$p$-adic Digit Position", fontsize=14, labelpad=10)
    ax.set_ylabel("Integer Value", fontsize=14, labelpad=10)
    ax.set_title(r"Binary ${p}$-adic Digit Patterns", fontsize=16, pad=20)

    # Customize ticks
    ax.set_xticks(np.arange(0, max_digits) + 0.4)
    ax.set_xticklabels([r"$a_{{{i}}}$".format(i=i) for i in range(max_digits)])
    ax.set_yticks(np.arange(0, max_value + 1) + 0.4)
    ax.set_yticklabels([str(i) for i in range(max_value + 1)])

    # Add colorbar
    cbar = plt.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, pad=0.02, fraction=0.046
    )
    cbar.set_label(r"Digit Value (base ${p}$)".format(p=p), fontsize=12, labelpad=10)

    # Add a descriptive caption
    caption = (
        r"Figure: Binary ${p}$-adic digit patterns for integers $0$ to ${max_value}$.".format(
            p=p, max_value=max_value
        )
        + "\n"
        + r"Each row represents an integer, and columns show the ${p}$-adic digits $a_i$ ".format(
            p=p
        )
        + r"where $\mathrm{val}_p(x) = \sum_{i=0}^{\infty} a_i p^i$."
    )
    plt.figtext(0.5, 0.01, caption, ha="center", fontsize=9, wrap=True)

    # Ensure the output directory exists
    os.makedirs("visualizations/output", exist_ok=True)

    # Save the figure with high resolution
    plt.savefig(f"visualizations/output/{filename}.pdf", bbox_inches="tight")
    plt.savefig(f"visualizations/output/{filename}.png", bbox_inches="tight")
    plt.close()

    print(f"Generated {filename}.pdf and {filename}.png in visualizations/output/")


# Generate visualizations for different primes
for p in [2, 3, 5]:
    visualize_padic_digits(p=p, filename=f"padic_digits_base_{p}")

print("All visualizations completed.")
