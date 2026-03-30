#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
from plots.graph_configs import scion_og

# =========================
# Configuration
# =========================

CSV_FILE = "results/outgoing_core_edges.csv"  # replace with your CSV path
ID_COLUMN = "edgelist_file"

# Metrics to plot
METRICS = ["outgoing_edges", "nodes_in_isd", "cheeger"]

OUTPUT_DIR = "plots/imgs/grouped_barplots"
FIGSIZE = (12, 10)  # taller for vertical stacking
BAR_WIDTH = 0.6
ROTATION = 45
DPI = 300
FILE_EXT = "png"

BASE_COLOR = scion_og.color
ALPHAS = [1.0, 0.7, 0.4]  # optional, can use same alpha for all

# =========================
# Helper functions
# =========================

def sanitize_filename(name: str) -> str:
    name = name.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-z0-9_\-]", "", name)
    return name

def extract_country(filename) -> str:
    filename = str(filename)
    match = re.search(r"_([A-Z]{2})_", filename)
    if match:
        return match.group(1)
    return filename

# =========================
# Load data
# =========================

df = pd.read_csv(CSV_FILE)
df["country"] = df[ID_COLUMN].astype(str).apply(extract_country)
df = df.sort_values("country").reset_index(drop=True)

# =========================
# Plotting
# =========================

n_metrics = len(METRICS)
n_countries = len(df)
x = np.arange(n_countries)

# Create vertically stacked subplots (n_metrics rows, 1 column)
fig, axes = plt.subplots(n_metrics, 1, figsize=FIGSIZE, sharex=True)

# Ensure axes is iterable
if n_metrics == 1:
    axes = [axes]

for ax, metric, alpha in zip(axes, METRICS, ALPHAS):
    ax.bar(
        x,
        df[metric],
        width=BAR_WIDTH,
        color=BASE_COLOR,
        alpha=alpha
    )
    ax.set_ylabel(metric)
    ax.grid(axis="y", alpha=0.3)

    # Set x labels on all subplots
    ax.set_xticks(x)
    ax.set_xticklabels(df["country"], rotation=ROTATION, ha="right")
    ax.tick_params(axis='x', labelbottom=True)

plt.tight_layout()

# Save figure
os.makedirs(OUTPUT_DIR, exist_ok=True)
filename = f"grouped_metrics_stacked.{FILE_EXT}"
plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=DPI)
plt.close(fig)
