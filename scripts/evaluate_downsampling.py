from metrics import metrics_basic
import pandas as pd
from pathlib import Path
import utils.io as io
import os

def save_metrics(name, graph_dict, output_folder):
    all_results = []

    for name, graph in graph_dict.items():
        results = metrics_basic.compute(graph)
        results["graph_idx"] = name
        all_results.append(results)

    new_data = pd.DataFrame([{"topology": name, **metrics} for name, metrics in all_results.items()])

    output_path = os.paths.join(output_folder, name)
    new_data.to_csv(output_path, index=False)
    print(f"Created new CSV at {output_path}")


def get_graph_dict(files):
    return {file.stem: io.load_graph(file) for file in files}
    

if __name__ == "__main__":
    caida_path = "data/20251201/caida_crve/"
    caida_folders = {folder.name: [file for file in folder.iterdir() if file.is_file()] for folder in Path(caida_path).iterdir() if folder.is_dir()}

    for foldername, folder in caida_folders.items():
        graph_dict = get_graph_dict(folder)
        save_metrics(foldername, graph_dict, "results/Downsampling")
