import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec

# Import the common matplotlib configuration
from visualizations.matplotlib_config import configure_matplotlib

# Apply the configuration
configure_matplotlib()


def visualize_predicate_evaluation(
    p=3,
    max_val=12,
    t_delta=5,
    w_delta=[0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005],
    C_delta=1.2,
    phi_function=None,
    filename="predicate_evaluation",
):
    """
    Visualize the evaluation of predicates of the form:
    P_Δ(binp(x)) = (val(x) < t_Δ) ∧ (∑ w_i(Δ) · φ(a_i) < C_Δ)

    Parameters:
    -----------
    p : int
        The prime base
    max_val : int
        Maximum value to compute evaluations for
    t_delta : float
        t_Δ parameter
    w_delta : list
        List of w_i(Δ) weights
    C_delta : float
        C_Δ threshold
    phi_function : function
        The φ function to apply to digits
    filename : str
        Base filename for saving the figure
    """
    # Set default phi_function if none provided
    if phi_function is None:
        phi_function = lambda x: x / p

    # Function to compute p-adic digits
    def padic_digits(n, p, digits):
        result = []
        for _ in range(digits):
            result.append(n % p)
            n //= p
        return result

    # Function to compute val_p(x)
    def val_p(n, p):
        if n == 0:
            return float("inf")
        val = 0
        while n % p == 0:
            n //= p
            val += 1
        return val

    # Create a larger figure with GridSpec for better layout
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, height_ratios=[1, 4], width_ratios=[3, 1])

    # Initialize subplots
    ax_val = fig.add_subplot(gs[0, 0])
    ax_sum = fig.add_subplot(gs[1, 0])
    ax_result = fig.add_subplot(gs[1, 1])
    ax_colorbar = fig.add_subplot(gs[0, 1])

    max_digits = len(w_delta)

    # Compute values for all integers up to max_val
    integers = list(range(max_val + 1))
    valuations = [val_p(n, p) for n in integers]

    # Compute p-adic digit expansions
    expansions = [padic_digits(n, p, max_digits) for n in integers]

    # Compute predicate components
    val_condition = [val < t_delta for val in valuations]

    # Compute the weighted sums
    weighted_sums = []
    for expansion in expansions:
        weighted_sum = sum(
            w * phi_function(digit) for w, digit in zip(w_delta, expansion)
        )
        weighted_sums.append(weighted_sum)

    sum_condition = [ws < C_delta for ws in weighted_sums]

    # Compute the final predicate results
    predicate_results = [v and s for v, s in zip(val_condition, sum_condition)]

    # Create a colormap for the visualization
    custom_cmap = LinearSegmentedColormap.from_list(
        "custom_cmap", ["#f7fbff", "#2171b5"], N=256
    )

    # Plot valuations
    ax_val.bar(
        integers,
        valuations,
        color="#6baed6",
        width=0.7,
        edgecolor="white",
        label=r"$\mathrm{val}_p(x)$",
    )
    ax_val.axhline(
        y=t_delta,
        color="red",
        linestyle="--",
        label=r"$t_\Delta = {0}$".format(t_delta),
    )
    ax_val.set_xlim(-0.5, max_val + 0.5)
    ax_val.set_xlabel("Integer $x$", fontsize=12, labelpad=10)
    ax_val.set_ylabel(r"$\mathrm{val}_p(x)$", fontsize=12, labelpad=10)
    ax_val.set_title(r"$\mathrm{val}_p(x) < t_\Delta$ Component", fontsize=14, pad=15)
    ax_val.legend(loc="upper right", frameon=True)

    # Plot the weighted sum visualization
    ax_sum.bar(
        integers,
        weighted_sums,
        color="#9ecae1",
        width=0.7,
        edgecolor="white",
        label=r"$\sum w_i(\Delta) \cdot \phi(a_i)$",
    )
    ax_sum.axhline(
        y=C_delta,
        color="red",
        linestyle="--",
        label=r"$C_\Delta = {0}$".format(C_delta),
    )
    ax_sum.set_xlim(-0.5, max_val + 0.5)
    ax_sum.set_xlabel("Integer $x$", fontsize=12, labelpad=10)
    ax_sum.set_ylabel("Weighted Sum", fontsize=12, labelpad=10)
    ax_sum.set_title(
        r"$\sum_{i=0}^{\infty} w_i(\Delta) \cdot \phi(a_i) < C_\Delta$ Component",
        fontsize=14,
        pad=15,
    )
    ax_sum.legend(loc="upper right", frameon=True)

    # Plot the final predicate result
    im = ax_result.imshow(
        [predicate_results],
        aspect="auto",
        cmap="RdYlGn",
        interpolation="none",
        extent=[-0.5, 0.5, -0.5, max_val + 0.5],
    )
    ax_result.set_yticks(np.arange(max_val + 1))
    ax_result.set_yticklabels([str(i) for i in integers])
    ax_result.set_xticks([0])
    ax_result.set_xticklabels(["Result"])
    ax_result.set_title("Predicate\nEvaluation", fontsize=14, pad=15)

    # Add text labels
    for i, result in enumerate(predicate_results):
        color = "white" if result else "black"
        text = "True" if result else "False"
        ax_result.text(0, i, text, ha="center", va="center", color=color, fontsize=8)

    # Display the formula
    formula = (
        r"$\mathcal{P}_\Delta(\mathrm{bin}_p(x)) = (\mathrm{val}_p(x) < t_\Delta) \wedge "
        r"(\sum_{i=0}^{\infty} w_i(\Delta) \cdot \phi(a_i) < C_\Delta)$"
    )

    # Show parameter values as a table in the upper right
    params_text = (
        f"Parameters:\n"
        r"$p = {0}$".format(p) + "\n"
        r"$t_\Delta = {0}$".format(t_delta) + "\n"
        r"$C_\Delta = {0}$".format(C_delta) + "\n"
        r"$\phi(a_i) = a_i/{0}$".format(p) + "\n"
        r"$w_i(\Delta) = $ {0}...".format(w_delta[:4])
    )

    # Add this to the colorbar axis which we'll use just for text
    ax_colorbar.axis("off")
    ax_colorbar.text(
        0.5,
        0.5,
        params_text,
        ha="center",
        va="center",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", fc="#f0f0f0", ec="black", lw=1),
    )

    # Add overall title
    plt.suptitle(formula, fontsize=16, y=0.98)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Add descriptive caption at the bottom
    caption = (
        r"Figure: Visualization of the predicate evaluation for test ideal membership. "
        r"The top panel shows the $p$-adic valuation compared to $t_\Delta = {0}$. ".format(
            t_delta
        )
        + r"The bottom left panel shows the weighted sum of the transformed digits compared to $C_\Delta = {0}$. ".format(
            C_delta
        )
        + r"The right panel shows the final evaluation result."
    )
    plt.figtext(0.5, 0.01, caption, ha="center", fontsize=9, wrap=True)

    # Save the figure with high resolution
    plt.savefig(f"visualizations/output/{filename}.pdf", bbox_inches="tight")
    plt.savefig(f"visualizations/output/{filename}.png", bbox_inches="tight")
    plt.close()

    print(f"Generated {filename}.pdf and {filename}.png in visualizations/output/")


if __name__ == "__main__":
    # Generate visualizations with different parameters
    visualize_predicate_evaluation(p=2, filename="predicate_evaluation_p2")
    visualize_predicate_evaluation(p=3, filename="predicate_evaluation_p3")
    visualize_predicate_evaluation(
        p=5, t_delta=3, C_delta=0.8, filename="predicate_evaluation_p5"
    )

    print("All predicate visualizations completed.")
