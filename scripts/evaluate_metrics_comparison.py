from metrics import metrics_complex, metrics_basic, spectral
import pandas as pd
from pathlib import Path
import utils.io as io

def run_all_metrics(name, G):
    results = {}
    results["graph_index"] = name
    results.update(metrics_basic.compute(G))
    results.update(metrics_complex.compute(G))
    results.update(spectral.compute(G))
    return results

def save_metrics(graph_dict, output_path):
    results = []

    for name, graph in graph_dict.items():
        results.append(run_all_metrics(name, graph))

    new_data = pd.DataFrame([{"topology": name, **metrics} for name, metrics in results.items()])

    new_data.to_csv(output_path, index=False)
    print(f"Created new CSV at {output_path}")
    

if __name__ == "__main__":
    caida_path = "data/20251201/caida_crve/20/"
    caida_files = list(Path(caida_path).glob("*.txt"))
    caida_graphs = {file.stem: io.load_graph(file) for file in caida_files}

    scion_isds = "data/20251201/scion_isd/edgelist_merged/"
    scion_isd_files = list(Path(scion_isds).glob("*.txt"))
    scion_core = "data/20251201/20251201.SCION_core_topo.txt"
    scion_graphs = {file.stem: io.load_graph(file) for file in scion_isd_files}

    scion_isd_files += scion_core
    expander_path = "data/expanders/"
    expander_files = list(Path(expander_path).glob("*.txt"))
    expander_graphs = {file.stem: io.load_graph(file) for file in expander_files}

    save_metrics(caida_graphs, "results/BGP_crve_20.csv")
    save_metrics(scion_graphs, "results/SCION_ISDs.csv")
    save_metrics(expander_graphs, "results/Expanders.csv")