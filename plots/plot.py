import pandas as pd
import matplotlib.pyplot as plt
from utils import io

input_path = io.user_input_path()
output_path = io.user_output_path()
df = pd.DataFrame(io.load_csv(input_path))

def extract_pct(name):
    return name.rsplit("_", 1)[1].split(".")[0]

df["pct"] = df["graph_index"].apply(extract_pct)
print(df)

metrics = [col for col in df.columns if col not in ["graph_index", "pct"]]

df["pct"] = df["pct"].astype(float)
df[metrics] = df[metrics].astype(float)

df = df.sort_values("pct", ascending=False)
print(df)

plt.figure(figsize=(16,8))

for metric in metrics:
    plt.figure()
    plt.plot(df["pct"], df[metric], marker="o")

    # Reverse x-axis so largest percentage is on the left
    plt.gca().invert_xaxis()

    # Show all percentage values on x-axis
    plt.xticks(df["pct"].values)

    plt.xlabel("Percentage remaining")
    plt.ylabel(metric)
    plt.title(f"{metric} vs Percentage")
    plt.grid(True)
    plt.tight_layout()

    save_path = f"plots/imgs/{output_path}/{metric}.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    print("Saved:", save_path)

for metric in metrics:
    # min-max normalization to [0,1]
    normalized = (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
    plt.plot(df["pct"], normalized, marker="o", label=metric, alpha=0.6)

plt.gca().invert_xaxis()                 
plt.xticks(df["pct"].values)            
plt.xlabel("Percentage remaining")
plt.ylabel("Normalized value (0-1)")
plt.title("All metrics normalized vs Percentage")
plt.legend(fontsize=8)
plt.grid(True)
plt.tight_layout(pad=3)  

save_path = f"plots/imgs/{output_path}/all_metrics_normalized.png"
plt.savefig(save_path, dpi=300)
plt.close()
print("Saved:", save_path)