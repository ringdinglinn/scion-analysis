#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from plots.mpl_config import apply_styling
from plots.graph_configs import scion_isd

apply_styling()

# =========================
# Configuration
# =========================

CSV_PATH = "results/SCION_ISDs_border_breadth.csv"

COUNTRY_COLUMN = "cc"
CHEEGER_COLUMN = "cheeger"
CORE_CONTROL_COLUMN = "core_control"

FIGSIZE = (12, 5)
BAR_WIDTH = 0.35
ROTATION = 45
DPI = 300

OUTPUT_DIR = "plots/imgs"
OUTPUT_FILE = "border_breadth_cheeger.pdf"

# =========================
# Load data
# =========================

df = pd.read_csv(CSV_PATH)

df = df.dropna(subset=[CHEEGER_COLUMN, CORE_CONTROL_COLUMN])
df = df.sort_values(by=COUNTRY_COLUMN)


countries = df[COUNTRY_COLUMN].tolist()
cheeger = df[CHEEGER_COLUMN].values
core_control = df[CORE_CONTROL_COLUMN].values

# =========================
# Plot
# =========================

x = np.arange(len(countries))

fig, ax = plt.subplots(figsize=FIGSIZE)

ax.bar(
    x - BAR_WIDTH / 2,
    cheeger,
    width=BAR_WIDTH,
    label="Intra-ISD Cheeger Constant",
    color=scion_isd.color,
)

ax.bar(
    x + BAR_WIDTH / 2,
    core_control,
    width=BAR_WIDTH,
    label="Border Breadth",
)

ax.set_xticks(x)
ax.set_xticklabels(countries, rotation=ROTATION, ha="right")

ax.set_ylabel("Value")
ax.set_xlabel("Country")
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()

os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.savefig(os.path.join(OUTPUT_DIR, OUTPUT_FILE), dpi=DPI)
plt.close(fig)
