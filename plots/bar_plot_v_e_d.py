import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import io
from plots.graph_configs import scion_og, scion_conn, caida_og, caida_conn
from plots.mpl_config import apply_styling

apply_styling()

class PlotConfig:
    def __init__(self, input_graphs, output_path):
        self.graphs = input_graphs
        self.output_path = output_path

configs = []

configs.append(PlotConfig(
    input_graphs=[
        caida_og, 
        scion_og
    ],
    output_path="CAIDA_vs_SCION"
))

configs.append(PlotConfig(
    input_graphs=[
        caida_og, 
        caida_conn
    ],
    output_path="CAIDA_downsample"
))

configs.append(PlotConfig(
    input_graphs=[
        scion_og,
        scion_conn
    ],
    output_path="SCION_edge_downsample"
))

configs.append(PlotConfig(
    input_graphs=[
        caida_og,
        caida_conn,
        scion_og,
        scion_conn
    ],
    output_path="CAIDA_SCION_downsampling"
))

for config in configs:

    graphs = config.graphs

    input_paths = [g.input_path for g in graphs]
    labels = [g.name for g in graphs]
    colors = [g.color for g in graphs]

    # -----------------------------
    # LOAD CSVs
    # -----------------------------
    dataframes = []
    for path in input_paths:
        df = pd.DataFrame(io.load_csv(path))
        df = df.apply(pd.to_numeric, errors="coerce")
        dataframes.append(df)

    # -----------------------------
    # SPECIFY METRICS
    # -----------------------------
    metrics = ["|V|", "|E|", "avg_degree"]
    metrics = [m for m in metrics if all(m in df.columns for df in dataframes)]
    dataframes = [df[metrics] for df in dataframes]

    # -----------------------------
    # AGGREGATE (MEAN / STD)
    # -----------------------------
    means, stds = [], []
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
    # PLOT
    # -----------------------------
    fig, axes = plt.subplots(
        1, 2, figsize=(12, 6),
        gridspec_kw={"width_ratios": [2, 1]}
    )

    num_datasets = len(labels)
    bar_width = 0.8 / num_datasets

    # ---- Subplot 1: |V| and |E| ----
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

        for j, bar in enumerate(bars):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 1.02,
                f"{values.iloc[j]:.0f}",
                ha="center",
                va="bottom",
                rotation=90,
                fontsize=8
            )

    ax.set_xticks(x)
    ax.set_xticklabels(metrics_ve)
    ax.set_ylabel("Count")
    ax.set_title("")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # ---- Subplot 2: avg_degree ----
    ax = axes[1]
    x = np.array([0])

    for i, label in enumerate(labels):
        value = means_df.loc[label, "avg_degree"]
        error = stds_df.loc[label, "avg_degree"]

        ax.bar(
            x + i * bar_width - 0.4 + bar_width / 2,
            value,
            bar_width,
            yerr=abs(error) if error != 0 else None,
            capsize=4 if error != 0 else 0,
            color=colors[i]
        )

        ax.text(
            x[0] + i * bar_width - 0.4 + bar_width / 2,
            value * 1.02,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            rotation=90,
            fontsize=8
        )

    ax.set_xticks(x)
    ax.set_xticklabels(["avg_degree"])
    ax.set_ylabel("Average Degree")
    ax.set_title("")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    for ax in axes:
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin, ymax * 1.1)

    fig.legend(
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.05),
        ncol = 2,
        frameon=False
    )
    plt.tight_layout(rect=[0, 0.15, 1, 1])
    plt.savefig(f"plots/imgs/bar_plots/{config.output_path}.png", dpi=300)
    plt.close()

    print(f"Saved: plots/imgs/bar_plots/{config.output_path}.png")