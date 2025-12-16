import pandas as pd
import matplotlib.pyplot as plt
from utils import io
import numpy as np

def find_intersections(x, y1, y2):
    intersections = []
    for i in range(len(x) - 1):
        y1_start, y1_end = y1[i], y1[i+1]
        y2_start, y2_end = y2[i], y2[i+1]

        # Check if lines cross between points
        if (y1_start - y2_start) * (y1_end - y2_end) < 0:
            # Linear interpolation to find crossing
            t = (y2_start - y1_start) / ((y1_end - y1_start) - (y2_end - y2_start))
            x_cross = x[i] + t * (x[i+1] - x[i])
            intersections.append(x_cross)
    return intersections

# -----------------------------
# INPUT / OUTPUT PATHS
# -----------------------------
input_path_1 = io.user_input_path()
input_path_2 = io.user_input_path(index=2)
output_path = io.user_output_path(index=3)

# -----------------------------
# LOAD DATA
# -----------------------------
df1 = pd.DataFrame(io.load_csv(input_path_1))
df2 = pd.DataFrame(io.load_csv(input_path_2))

basic_metrics = ["avg_degree"]  # only avg_degree
complex_metrics = [
    "|V|",
    "|E|",
    "nr_connected_components",
    "degree_std",
    "degree_entropy",
    "assortativity",
    "transitivity",
    "average_clustering",
    "cheeger constant",
    "n_spanning_trees",
    "treewidth",
    "natural connectivity",
    "spectral gap",
    "spectral radius",
    "effective graph resistance",
    "algebaric connectivity",
]
all_metrics = basic_metrics + complex_metrics


# -----------------------------
# UTILITIES
# -----------------------------
def extract_pct(name):
    return name.rsplit("_", 1)[1].split(".")[0]


def compute_global_minmax(dfs, metric_columns):
    all_concat = pd.concat([df[metric_columns] for df in dfs], axis=0)
    return all_concat.min(), all_concat.max()


def normalize_df(df, metric_columns, global_min, global_max):
    for metric in metric_columns:
        min_v = 0
        max_v = global_max[metric]
        if max_v == min_v:
            df[metric] = 0.0
        else:
            df[metric] = (df[metric] - min_v) / (max_v - min_v)
    return df


def prepare_df(df):
    df["pct"] = df["graph_index"].apply(extract_pct).astype(float)
    df[all_metrics] = df[all_metrics].astype(float)
    df = df.sort_values("pct", ascending=False)
    return df


# -----------------------------
# PREPARE DATA
# -----------------------------
df1 = prepare_df(df1)
df2 = prepare_df(df2)
df2_pct_value = df2["pct"].iloc[0]


# -----------------------------
# 2. COMBINED PLOT (NORMALIZED)
# -----------------------------
# Normalize
global_min, global_max = compute_global_minmax([df1, df2], all_metrics)
df1_norm = normalize_df(df1.copy(), all_metrics, global_min, global_max)
df2_norm = normalize_df(df2.copy(), all_metrics, global_min, global_max)

plt.figure(figsize=(16, 8))
metric_colors = {}
metric_colors["avg_degree"] = "black"

# Complex metrics for df1
for metric in complex_metrics:
    line, = plt.plot(df1_norm["pct"], df1_norm[metric], marker="o", alpha=0.85, linewidth=2, label=f"df1 {metric}")
    metric_colors[metric] = line.get_color()

# Complex metrics for df2
for metric in complex_metrics:
    plt.axhline(y=df2_norm[metric].iloc[0], linestyle="--", linewidth=1.6,
                color=metric_colors[metric], alpha=0.9, label=f"df2 {metric} (pct={df2_pct_value})")

# avg_degree for df1
line, = plt.plot(df1_norm["pct"], df1_norm["avg_degree"], alpha=0.55, linestyle="-", linewidth=1.8, label="df1 avg_degree", color=metric_colors["avg_degree"])

# avg_degree for df2
plt.axhline(y=df2_norm["avg_degree"].iloc[0], linestyle="--", linewidth=1.4,
            color=metric_colors["avg_degree"], alpha=0.85, label="df2 avg_degree")

# Formatting
plt.gca().invert_xaxis()
plt.xticks(df1["pct"].values)
plt.xlabel("Percentage remaining")
plt.ylabel("Normalized value (0–1)")
plt.title("Normalized Comparison: Complex Metrics vs Avg Degree")
plt.legend(fontsize=8, ncol=2)
plt.tight_layout(pad=3)

# Save
save_path = f"plots/imgs/{output_path}_all_complex_metrics_norm.png"
plt.savefig(save_path, dpi=300)
plt.close()
print("Saved:", save_path)


# -----------------------------
# 1. PLOTS PER COMPLEX METRIC (TWO Y-AXES)
# -----------------------------
for metric in complex_metrics:

    fig, ax1 = plt.subplots(figsize=(16, 8))

    # Left y-axis: complex metric for df1
    color_metric = metric_colors[metric]
    ax1.set_xlabel("Percentage remaining")
    ax1.set_ylabel(metric, color=color_metric)
    line1, = ax1.plot(df1["pct"], df1[metric], marker="o", linewidth=2, color=color_metric, label=f"SCION {metric}")
    ax1.tick_params(axis='y', labelcolor=color_metric)
    plt.xticks(df1["pct"].values)

    # Horizontal line for df2 metric
    ax1.axhline(y=df2[metric].iloc[0], linestyle="--", linewidth=1.6,
                color=color_metric,  label=f"CAIDA {metric} (pct={df2_pct_value})")

    # Right y-axis: average degree
    ax2 = ax1.twinx()
    color_deg = metric_colors["avg_degree"]
    ax2.set_ylabel("Average Degree", color=color_deg)
    ax2.plot(df1["pct"], df1["avg_degree"], linestyle="-", linewidth=1.5, color=color_deg, label="SCION avg_degree")
    ax2.axhline(y=df2["avg_degree"].iloc[0], linestyle="--", linewidth=1.6, color=color_deg, label="CAIDA avg_degree")
    ax2.tick_params(axis='y', labelcolor=color_deg)

    # Optional: intersections
    x = df1["pct"].values
    y1 = df1[metric].values
    y2 = np.full_like(x, df2[metric].iloc[0])
    cross_pts = find_intersections(x, y1, y2)
    if len(cross_pts) > 0:
        ax1.axvline(x=cross_pts[0], linestyle=":", color=color_metric, label="Metric Intersection")

    y_avg = df1["avg_degree"].values
    y_avg_hline = np.full_like(x, df2["avg_degree"].iloc[0])
    cross_pts = find_intersections(x, y_avg, y_avg_hline)
    if len(cross_pts) > 0:
        ax2.axvline(x=cross_pts[0], linestyle=":", color=color_deg, label="Avg Degree Intersection")

    # Formatting
    ax1.invert_xaxis()
    plt.title(f"{metric} vs Average Degree (Raw Values)")

    # Combine legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, fontsize=8)

    plt.tight_layout(pad=3)

    # Save
    save_path = f"plots/imgs/{output_path}_{metric}_raw.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print("Saved:", save_path)

