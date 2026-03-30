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
    "SCION Core",
    "results/SCION_ISDs_core.csv",
    "#184D85"
)

scion_conn = GraphConfig(
    "SCION connectivity edge deletion",
    "results/SCION_conn_12.45.csv",
    "#6fa1cd"
)

# -----------------------------
# CAIDA datasets
# -----------------------------
caida_og = GraphConfig(
    "CAIDA Sep 2025",
    "results/CAIDA_20251201_basics.csv",
    "#D85652"
)

caida_conn = GraphConfig(
    "CAIDA crve + connectivity downsample",
    "results/CAIDA_20251201_crve_complex.csv",
    "#BF332C"
)


expander = GraphConfig(
    "Expander graph",
    'results/Expander_complex_metrics.csv',
    "#64B142"
)