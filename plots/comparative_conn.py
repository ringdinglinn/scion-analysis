import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from plots.mpl_config import apply_styling
from plots.graph_configs import caida_og
import re
from plots.metric_utils import METRICS

def extract_number(path: Path) -> int:
    numbers = re.findall(r"\d+", path.stem)
    return int(numbers[-1])

apply_styling()

FIGURES = [
    [
        ["|V|", "|E|", "avg_degree"],
        ["assortativity", "degree_std", "degree_entropy"],
    ]
]

# -------- Configuration --------
csv_dir = Path("./results/CRVE/")
variation = "std"
outpath = Path("./plots/imgs/crve")
# --------------------------------

csv_files = sorted(csv_dir.glob("*.csv"), key=extract_number)
dataframes = [pd.read_csv(f) for f in csv_files]
x_labels = [extract_number(f) for f in csv_files]
x = list(range(len(csv_files)))

print(len(dataframes))

# Extract metric names
metrics = [col for col in dataframes[0].columns if col != "graph_index"]

x = list(range(len(csv_files)))

from plots.metric_utils import METRICS

for fig_idx, grid in enumerate(FIGURES):
    n_rows = len(grid)
    n_cols = len(grid[0])

    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(4 * n_cols, 3 * n_rows),
        sharex=True
    )

    # Normalize axes to 2D
    if n_rows == 1:
        axes = [axes]
    if n_cols == 1:
        axes = [[ax] for ax in axes]

    for r, row in enumerate(grid):
        for c, metric in enumerate(row):
            ax = axes[r][c]

            means = []
            vars_ = []

            for df in dataframes:
                values = df[metric]
                means.append(values.mean())
                vars_.append(values.sem() if variation == "sem" else values.std())

            vars_ = [0.0 if pd.isna(v) else v for v in vars_]
            lower = [m - v for m, v in zip(means, vars_)]
            upper = [m + v for m, v in zip(means, vars_)]

            ax.plot(x, means, linewidth=1, color=caida_og.color, marker=".")
            ax.fill_between(x, lower, upper, color=caida_og.color, alpha=0.3)

            if metric == "assortativity":
                ax.set_ylim(-1.05, 0.05)
            else:
                y_max = max(upper)
                headroom = 0.05 * y_max if y_max > 0 else 1.0
                ax.set_ylim(0, y_max + headroom)


            ax.grid(True)
            pad = 0.3 
            ax.set_xlim(len(x) - 1 + pad, -pad)
            ax.set_ylabel(METRICS.get(metric, metric))

            if r == n_rows - 1:
                ax.set_xticks(x)
                ax.set_xticklabels(x_labels)
                ax.set_xlabel(r"Remaining Percentage, $\%$")


    fig.tight_layout()
    fig.savefig(
        outpath / f"crve_combined_{fig_idx}.pdf",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
