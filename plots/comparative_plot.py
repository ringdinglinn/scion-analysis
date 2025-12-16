import pandas as pd
import matplotlib.pyplot as plt
from utils import io

input_path_1 = io.user_input_path()
input_path_2 = io.user_input_path(index=2)
output_path = io.user_output_path(index=3)

df1 = pd.DataFrame(io.load_csv(input_path_1))
df2 = pd.DataFrame(io.load_csv(input_path_2))

basic_metrics = ["|V|", "|E|", "avg_degree"]
complex_metrics = ["algebraic connectivity", "cheeger constant"]  # add more if present
all_metrics = basic_metrics + complex_metrics


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


# Prepare
df1 = prepare_df(df1)
df2 = prepare_df(df2)

# Normalize
global_min, global_max = compute_global_minmax([df1, df2], all_metrics)
df1 = normalize_df(df1, all_metrics, global_min, global_max)
df2 = normalize_df(df2, all_metrics, global_min, global_max)

# The pct for df2 is a single value:
df2_pct_value = df2["pct"].iloc[0]


# -------------------------------------------------------------
#    CREATE ONE PLOT PER COMPLEX METRIC
# -------------------------------------------------------------

for metric in complex_metrics:

    plt.figure(figsize=(16, 8))
    metric_colors = {}

    # 1. Plot the complex metric for df1
    line, = plt.plot(
        df1["pct"],
        df1[metric],
        marker="o",
        alpha=0.8,
        linewidth=2.0,
        label=f"df1 {metric}",
    )
    metric_colors[metric] = line.get_color()

    # 2. Vertical line for df2
    plt.axhline(
        y=df2[metric].iloc[0],
        linestyle="--",
        linewidth=1.6,
        color=metric_colors[metric],
        alpha=0.9,
        label=f"df2 {metric} (pct={df2_pct_value})"
    )

    # 3. Plot the three basic metrics for df1 (line plots)
    for basic in basic_metrics:
        line, = plt.plot(
            df1["pct"],
            df1[basic],
            alpha=0.55,
            linestyle="-",
            linewidth=1.5,
            label=f"df1 {basic}",
        )
        metric_colors[basic] = line.get_color()

    # 4. Horizontal lines for df2 for the basic metrics
    for basic in basic_metrics:
        plt.axhline(
            y=df2[basic].iloc[0],
            linestyle="--",
            linewidth=1.2,
            alpha=0.85,
            color=metric_colors[basic],
            label=f"df2 {basic}",
        )

    # 5. Final formatting
    plt.gca().invert_xaxis()
    plt.xticks(df1["pct"].values)
    plt.xlabel("Percentage remaining")
    plt.ylabel("Normalized value (0–1)")
    plt.title(f"Normalized Comparison: {metric}")
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.tight_layout(pad=3)

    # Save
    save_path = f"plots/imgs/{output_path}_{metric}.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print("Saved:", save_path)
