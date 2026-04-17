#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
from plots.mpl_config import apply_styling
from plots.graph_configs import scion_isd, scion_core, caida, expander
from plots.metric_utils import METRICS

apply_styling()

# =========================
# Configuration
# =========================

CSV_MAIN = "results/SCION_ISDs.csv"

EXTRA_DATASETS = [
    {
        "name": "BGP, CRVE 20%",
        "csv": "results/BGP_crve_20.csv",
        "color": caida.color,
    },
    {
        "name": "Expander",
        "csv": "results/Expanders.csv",
        "color": expander.color,
    },
]

COUNTRIES = [
    'AU', 'BR', 'CN', 'FR', 'DE', 'IN', 'IR', 'IT',
    'NL', 'RU', 'SG', 'ZA', 'CH', 'UA', 'GB', 'US'
]

MANUAL_LABELS = {
    "20251201.SCION_core_topo.txt": "SCION CORE",
}

FIGURES = [
    [
        ["|V|", "|E|"],
        ["avg_degree", "assortativity"],
        ["degree_std", "degree_entropy"],
    ],
    [
        ["avg_degree", "cheeger_constant"],
        ["algebraic_connectivity", "spectral_gap"],
    ],
    [   
        ["avg_degree"],
        ["cheeger_constant"]
    ]
]

ID_COLUMN = "graph_index"

FIGSIZE = (10, 5)
ERROR_CAPSIZE = 5
ROTATION = 45
BAR_WIDTH = 0.4

COLOR_MAIN = scion_isd.color
COLOR_MANUAL = scion_core.color

OUTPUT_DIR = "plots/imgs/metrics_comparison"
DPI = 300
FILE_EXT = "pdf"

# =========================
# Helpers
# =========================

def sanitize_filename(name: str) -> str:
    name = name.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-z0-9_\-]", "", name)
    return name


def resolve_label(label: str, countries: list[str], manual_labels: dict) -> tuple[str, bool]:
    base = os.path.basename(label)

    for key, value in manual_labels.items():
        if key in base:
            return value, True

    for c in countries:
        if f"_{c}_" in base or base.endswith(f"_{c}") or base.startswith(f"{c}_"):
            return c, False

    return base, False


def plot_metric_on_ax(ax, metric, df_main, extra_stats, single_samples=None):
    df_sorted = df_main.sort_values(by=ID_COLUMN)
    x_main = np.arange(len(df_sorted))

    resolved = [
        resolve_label(label, COUNTRIES, MANUAL_LABELS)
        for label in df_sorted[ID_COLUMN].values
    ]

    main_labels = [lbl for lbl, _ in resolved]
    main_colors = [
        COLOR_MANUAL if is_manual else COLOR_MAIN
        for _, is_manual in resolved
    ]

    # Main bars
    ax.bar(
        x_main,
        df_sorted[metric].values,
        color=main_colors,
        width=BAR_WIDTH,
    )

    # Extra datasets (mean ± std)
    x_extra_start = len(x_main)
    x_extra = np.arange(x_extra_start, x_extra_start + len(extra_stats))

    for x, stats in zip(x_extra, extra_stats):
        std_val = stats["std"][metric]
        std_val = np.asarray(std_val).squeeze().item() if np.size(std_val) == 1 else 0.0

        ax.bar(
            x,
            stats["mean"][metric],
            yerr=None if np.isclose(std_val, 0.0) else std_val,
            capsize=ERROR_CAPSIZE,
            color=stats["color"],
            width=BAR_WIDTH,
        )

    labels = main_labels + [f'{s["name"]} (avg)' for s in extra_stats]
    xticks = np.concatenate([x_main, x_extra])

    if single_samples:
        for idx, sample in enumerate(single_samples):
            x = x_extra_start + len(extra_stats) + idx
            ax.bar(
                x,
                sample["values"][metric],
                color=sample["color"],
                width=BAR_WIDTH,
            )
            xticks = np.append(xticks, x)
            labels.append(sample["name"])

    ax.set_xticks(xticks)
    ax.set_xticklabels(labels, rotation=ROTATION, ha="right", fontsize=17)
    ax.grid(axis="y", alpha=0.3)

# =========================
# Load main data
# =========================

df_main = pd.read_csv(CSV_MAIN)
metrics = [m for layout in FIGURES for row in layout for m in row]

# =========================
# Load and compute extra dataset stats
# =========================

extra_stats = []

for ds in EXTRA_DATASETS:
    df = pd.read_csv(ds["csv"])
    # small fix for assortativity = NaN for expanders
    # NaN is mapped to 0 for visualization 

    df["assortativity"] = df["assortativity"].fillna(0.0)

    missing_metrics = [m for m in metrics if m not in df.columns]
    if missing_metrics:
        raise ValueError(
            f"Dataset {ds['csv']} is missing metrics: {missing_metrics}"
        )

    extra_stats.append({
        "name": ds["name"],
        "color": ds["color"],
        "mean": df[metrics].mean().to_dict(),
        "std": df[metrics].std().to_dict(),
    })

# =========================
# Load single-sample datasets
# =========================

single_samples = []

def load_single_sample(cfg, enable_flag):
    if not enable_flag:
        return None

    df = pd.read_csv(cfg["csv"])

    missing_metrics = [m for m in metrics if m not in df.columns]
    if missing_metrics:
        raise ValueError(
            f'{cfg["name"]} dataset is missing metrics: {missing_metrics}'
        )

    if len(df) != 1:
        raise ValueError(
            f'{cfg["name"]} dataset must contain exactly one row'
        )

    return {
        "name": cfg["name"],
        "color": cfg["color"],
        "values": df.iloc[0],
    }

# =========================
# Prepare output directory
# =========================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Plotting combined figures
# =========================

for fig_idx, layout in enumerate(FIGURES):
    nrows = len(layout)
    ncols = len(layout[0])

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(FIGSIZE[0] * ncols, FIGSIZE[1] * nrows),
        squeeze=False,
    )

    metrics = set()

    for i, row in enumerate(layout):
        for j, metric in enumerate(row):
            ax = axes[i, j]
            plot_metric_on_ax(
                ax,
                metric,
                df_main,
                extra_stats,
                single_samples,
            )
            ax.set_ylabel(METRICS.get(metric, metric), fontsize=19)

            if i < nrows - 1:
                ax.set_xticklabels([])
            
            metrics.add(metric)

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    name = "_".join(sorted(set(metrics)))
    filename = f"{name}.{FILE_EXT}"
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=DPI)
    plt.close(fig)