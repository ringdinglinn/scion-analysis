# graph_configs.py

class GraphConfig:
    def __init__(self, name, color):
        self.name = name
        self.color = color

scion_core = GraphConfig(
    "SCION Core",
    "#184D85"
)

scion_isd = GraphConfig(
    "SCION ISD",
    "#6fa1cd"
)

caida = GraphConfig(
    "CAIDA crve + connectivity downsample",
    "#BF332C"
)

expander = GraphConfig(
    "Expander graph",
    "#64B142"
)