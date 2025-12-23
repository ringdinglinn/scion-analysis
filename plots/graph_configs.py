# graph_configs.py

class GraphConfig:
    def __init__(self, name, input_path, color):
        self.name = name
        self.input_path = input_path
        self.color = color

# -----------------------------
# SCION datasets
# -----------------------------
scion_og = GraphConfig(
    "SCION Jan 2023",
    "/Users/linn/Documents/01 UZH/MA/evaluation/results/SCION_complex.csv",
    "#760400"
)

scion_conn = GraphConfig(
    "SCION connectivity edge deletion",
    "/Users/linn/Documents/01 UZH/MA/evaluation/results/SCION_conn.csv",
    "#c04741"
)

# -----------------------------
# CAIDA datasets
# -----------------------------
caida_og = GraphConfig(
    "CAIDA Sep 2025",
    "/Users/linn/Documents/01 UZH/MA/evaluation/results/CAIDA_basics.csv",
    "#044387"
)

caida_conn = GraphConfig(
    "CAIDA crve + connectivity downsample",
    "/Users/linn/Documents/01 UZH/MA/evaluation/results/CAIDA_crve_10_conn_complex.csv",
    "#67b2f4"
)


expander = GraphConfig(
    "Expander graph",
    '/Users/linn/Documents/01 UZH/MA/evaluation/results/Expander_complex_metrics.csv',
    "#46B142"
)