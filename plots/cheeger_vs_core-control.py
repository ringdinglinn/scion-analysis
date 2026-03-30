#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from plots.mpl_config import apply_styling
from plots.graph_configs import scion_conn

apply_styling()


# =========================
# Configuration
# =========================

SCION_CSV = "results/SCION_ISDs.csv"
RATIO_CSV = "results/outgoing_core_edges.csv"

ID_COLUMN = "graph_index"
CHEEGER_COLUMN = "cheeger constant"

FIGSIZE = (12, 5)
BAR_WIDTH = 0.35
ROTATION = 45
DPI = 300

OUTPUT_DIR = "plots/imgs"
OUTPUT_FILE = "cheeger_vs_outgoing_ratio.pdf"

# =========================
# Helpers
# =========================

def extract_country(filename: str) -> str:
    """
    Extract country code from filenames like:
    20251201_scion_isd_NL_core.txt
    """
    m = re.search(r"_([A-Z]{2})_", filename)
    if m:
        return m.group(1)
    else:
        return None
    
# =========================
# Load SCION cheeger constants
# =========================

df_scion = pd.read_csv(SCION_CSV)

df_scion["country"] = df_scion[ID_COLUMN].apply(extract_country)
df_scion = df_scion.set_index("country")

cheeger = df_scion[CHEEGER_COLUMN]

# =========================
# Load outgoing-edge ratios
# =========================

df_ratio = pd.read_csv(RATIO_CSV)

df_ratio["country"] = df_ratio["edgelist_file"].apply(extract_country)
df_ratio["outgoing_ratio"] = (
    df_ratio["outgoing_edges"] / df_ratio["nodes_in_isd"]
)

df_ratio = df_ratio.set_index("country")

# =========================
# Align datasets
# =========================

common_countries = sorted(set(cheeger.index) & set(df_ratio.index))

cheeger = cheeger.loc[common_countries]
out_ratio = df_ratio.loc[common_countries, "outgoing_ratio"]

# =========================
# Plot
# =========================

x = np.arange(len(common_countries))

fig, ax = plt.subplots(figsize=FIGSIZE)

ax.bar(
    x - BAR_WIDTH / 2,
    cheeger.values,
    width=BAR_WIDTH,
    label="Cheeger constant intra-ISD, $r = 0.45, m = 0.05$",
    color=scion_conn.color
)

ax.bar(
    x + BAR_WIDTH / 2,
    out_ratio.values,
    width=BAR_WIDTH,
    label="Core Control",
)

ax.set_xticks(x)
ax.set_xticklabels(common_countries, rotation=ROTATION, ha="right")

ax.set_ylabel("Value")
ax.set_xlabel("Country")
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()

os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.savefig(os.path.join(OUTPUT_DIR, OUTPUT_FILE), dpi=DPI)
plt.close(fig)

# =========================
# End of script
# =========================
