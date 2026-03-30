import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import io
from plots.graph_configs import scion_og, caida_conn, expander
from plots.mpl_config import apply_styling

apply_styling()

class PlotConfig:
    def __init__(self, input_graphs, output_path):
        self.graphs = input_graphs
        self.output_path = output_path

configs = []

configs.append(PlotConfig(
    input_graphs=[
        caida_conn,
        scion_og,
        expander
    ],
    output_path="CAIDA_vs_SCION"
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
    metrics = list(dataframes[0].columns)
    excluded_cols = ["assortativity", "graph_index", "nr_connected_components"]
    metrics = [m for m in metrics if all(m in df.columns for df in dataframes) and m not in excluded_cols]
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
    # -----------------------------
    # NORMALIZE METRICS
    # -----------------------------
    all_values = pd.concat(dataframes, keys=labels)  # combine all for max calculation
    max_values = all_values.max(axis=0)  # max per metric

    # Compute normalized values and store for plotting
    norm_means = []
    for df in dataframes:
        norm_df = df[metrics] / max_values
        if len(df) == 1:
            norm_means.append(norm_df.iloc[0])
        else:
            norm_means.append(norm_df.mean(axis=0))

    norm_means_df = pd.DataFrame(norm_means, index=labels)

    # -----------------------------
    # PLOT NORMALIZED
    # -----------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    num_datasets = len(labels)
    num_metrics = len(metrics)
    x = np.arange(num_metrics)
    bar_width = 0.8 / num_datasets

    for i, label in enumerate(labels):
        values = norm_means_df.loc[label]
        bars = ax.bar(
            x + i * bar_width - 0.4 + bar_width / 2,
            values,
            bar_width,
            color=colors[i],
            label=label
        )

        # Annotate with absolute values from original means
        for j, bar in enumerate(bars):
            abs_val = means_df.loc[label, metrics[j]]  # original absolute value
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.02,
                f"{abs_val:.2f}" if abs_val % 1 else f"{int(abs_val)}",
                ha='center',
                va='bottom',
                rotation=90,
                fontsize=8
            )

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=-45, ha='left')
    ax.set_ylabel("Normalized Value (max = 1)")
    ax.set_title("Normalized Metrics Across Datasets")
    fig.legend(
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.05),
        ncol = 2,
        frameon=False
    )
    plt.tight_layout(rect=[0, 0.15, 1, 1])
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax * 1.1)

    plt.savefig(f"plots/imgs/bar_plots/{config.output_path}_normalized.png", dpi=300)
    plt.close()

    print(f"Saved: plots/imgs/bar_plots/{config.output_path}_normalized.png")
