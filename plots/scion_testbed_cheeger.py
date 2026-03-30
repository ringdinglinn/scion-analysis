#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from plots.mpl_config import apply_styling
from plots.graph_configs import scion_conn, caida_conn, expander

apply_styling()

# =========================
# Hardcoded data
# =========================

labels = ["Global CC", "BB", "Intra-ISD CC"]

values_og = [0.2, 0.4, 2.0]
values_re = [0.4, 0.8, 2.0]

# =========================
# Plot
# =========================

BAR_WIDTH = 0.35
FIGSIZE = (6, 4)
ROTATION = 0
DPI = 300

x = np.arange(len(labels))

fig, ax = plt.subplots(figsize=FIGSIZE)

ax.bar(
    x - BAR_WIDTH / 2,
    values_og,
    width=BAR_WIDTH,
    color="orange",
    alpha=1.0,
    label="Original topology"
)

ax.bar(
    x + BAR_WIDTH / 2,
    values_re,
    width=BAR_WIDTH,
    color="orange",
    alpha=0.6,
    label="Rewired topology"
)

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=ROTATION)
ax.set_ylabel("Metric value")

ax.grid(axis="y", alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig("plots/imgs/scion_testbed_cheeger_rewire.pdf", dpi=DPI)
plt.close(fig)
