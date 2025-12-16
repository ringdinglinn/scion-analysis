import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import io

# -----------------------------
# INPUT FILES
# -----------------------------
caida_path = io.user_input_path(index=1)
scion_path = io.user_input_path(index=2)
expander_path = io.user_input_path(index=3)
output_path = io.user_output_path(index=4)

# -----------------------------
# LOAD CSVs
# -----------------------------
caida_df = pd.DataFrame(io.load_csv(caida_path))      # single row
scion_df = pd.DataFrame(io.load_csv(scion_path))      # single row
expander_df = pd.DataFrame(io.load_csv(expander_path))  # multiple rows

# -----------------------------
# SPECIFY METRICS TO DISPLAY
# -----------------------------
metrics = [
    "|V|",
    "|E|",
    "avg_degree",
    "degree_std",
    "transitivity",
    "average_clustering",
    "cheeger constant",
    "treewidth"
]

metrics = [
    m for m in metrics
    if m in caida_df.columns and m in scion_df.columns and m in expander_df.columns
]

caida_df = caida_df[metrics]
scion_df = scion_df[metrics]
expander_df = expander_df[metrics]

caida_df = caida_df.apply(pd.to_numeric)
scion_df = scion_df.apply(pd.to_numeric)
expander_df = expander_df.apply(pd.to_numeric)

# -----------------------------
# PREPARE NORMALIZED VALUES
# -----------------------------
expander_df_mean = expander_df.mean(axis=0)
expander_mean_df = expander_df_mean.to_frame().T

max_values = pd.concat(
    [caida_df, scion_df, expander_mean_df],
    axis=0
).max(axis=0)

caida_values = (caida_df.iloc[0] / max_values).values
scion_values = (scion_df.iloc[0] / max_values).values
expander_means = (expander_mean_df.iloc[0] / max_values).values

x = np.arange(len(metrics))
width = 0.25

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(max(10, len(metrics) * 0.8), 6))

ax.bar(x - width, caida_values, width, label="CAIDA")
ax.bar(x, scion_values, width, label="SCION")
ax.bar(x + width, expander_means, width, label="Expander (mean)")

# Formatting
ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=45, ha="right")
ax.set_ylabel("Relative Metric Value (max = 1)")
ax.set_title("Comparison of Metrics Across Files (Normalized)")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()

# -----------------------------
# SAVE
# -----------------------------
plt.savefig(
    f"plots/imgs/{output_path}_comparison_barplot_normalized.png",
    dpi=300
)
plt.close()

print(
    "Saved:",
    f"plots/imgs/{output_path}_comparison_barplot_normalized.png"
)
