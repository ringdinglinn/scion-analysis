import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import io

# -----------------------------
# INPUT FILES (ANY NUMBER)
# -----------------------------
input_paths = io.user_input_paths()
output_path = io.user_output_path_last()

print(input_paths)
print(output_path)

# -----------------------------
# LOAD CSVs
# -----------------------------
dataframes = []
labels = []

for path in input_paths:
    df = pd.DataFrame(io.load_csv(path))
    df = df.apply(pd.to_numeric, errors="coerce")
    dataframes.append(df)
    labels.append(path.split("/")[-1].replace(".csv", ""))

# -----------------------------
# SPECIFY METRICS
# -----------------------------
metrics = ["|V|", "|E|", "avg_degree"]

# Keep only metrics present in all CSVs
metrics = [m for m in metrics if all(m in df.columns for df in dataframes)]
dataframes = [df[metrics] for df in dataframes]

# -----------------------------
# AGGREGATE (MEAN / STD)
# -----------------------------
means = []
stds = []

for df in dataframes:
    if len(df) == 1:
        means.append(df.iloc[0])
        stds.append(pd.Series(0, index=metrics))
    else:
        means.append(df.mean(axis=0))
        stds.append(df.std(axis=0))

means_df = pd.DataFrame(means, index=labels)
stds_df = pd.DataFrame(stds, index=labels)

# -----------------------------
# PLOT IN ONE FIGURE
# -----------------------------
fig, axes = plt.subplots(
    1, 2,
    figsize=(12, 6),
    gridspec_kw={"width_ratios": [2, 1]}
)
num_datasets = len(labels)
bar_width = 0.8 / num_datasets
colors = plt.cm.tab10.colors  # distinct colors per dataset

# =============================
# Subplot 1: |V| and |E|
# =============================
ax = axes[0]
metrics_ve = ["|V|", "|E|"]
x = np.arange(len(metrics_ve))

for i, label in enumerate(labels):
    values = means_df.loc[label, metrics_ve]
    errors = stds_df.loc[label, metrics_ve].abs() if stds_df.loc[label, metrics_ve].any() else None

    bars = ax.bar(
        x + i * bar_width - 0.4 + bar_width / 2,
        values,
        bar_width,
        yerr=errors,
        capsize=4 if errors is not None else 0,
        color=colors[i],
        label=label
    )

    # Annotations
    for j, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.02 * values.max(),
            f"{values.iloc[j]:.0f}",
            ha="center",
            va="bottom",
            rotation=90,
            fontsize=8
        )

ax.set_xticks(x)
ax.set_xticklabels(metrics_ve)
ax.set_ylabel("Count")
ax.set_title("|V| and |E|")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.6)

# =============================
# Subplot 2: avg_degree
# =============================
ax = axes[1]
x = np.array([0])  # single bar group

for i, label in enumerate(labels):
    value = means_df.loc[label, "avg_degree"]
    error = stds_df.loc[label, "avg_degree"]


    ax.bar(
        x + i * bar_width - 0.4 + bar_width / 2,
        value,
        bar_width,
        yerr=abs(error) if error != 0 else None,
        capsize=4 if error != 0 else 0,
        color=colors[i],
        label=label
    )

    ax.text(
        x[0] + i * bar_width - 0.4 + bar_width / 2,
        value + 0.02 * means_df["avg_degree"].max(),
        f"{value:.2f}",
        ha="center",
        va="bottom",
        rotation=90,
        fontsize=8
    )

for ax in axes:
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax * 1.1)

ax.set_xticks(x)
ax.set_xticklabels(["avg_degree"])
ax.set_ylabel("Average Degree")
ax.set_title("Average Degree")
ax.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig(f"plots/imgs/{output_path}_combined.png", dpi=300)
plt.close()

print("Saved:", f"plots/imgs/{output_path}_combined.png")
