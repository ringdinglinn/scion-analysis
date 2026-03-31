from metrics import metrics_basic
import pandas as pd
from pathlib import Path
import utils.io as io
import os

def save_metrics(foldername, graph_dict, output_folder):
    all_results = []

    for name, graph in graph_dict.items():
        print("name", name)
        results = metrics_basic.compute(graph)
        results["graph_idx"] = name
        all_results.append(results)

    data = pd.DataFrame(all_results)

    filename = next(iter(graph_dict.keys())).rsplit('_', 1)[0] + ".csv"
    output_path = os.path.join(output_folder, filename)
    data.to_csv(output_path, index=False)
    print(f"Created new CSV at {output_path}")


def get_graph_dict(files):    
    return {io.load_graph(file)[0]:io.load_graph(file)[1] for file in files}
    

if __name__ == "__main__":
    caida_path = "data/20251201/caida_crve/"
    caida_folders = {folder.name: [file for file in folder.iterdir() if file.is_file()] for folder in Path(caida_path).iterdir() if folder.is_dir()}

    
    
    for foldername, folder in caida_folders.items():
        graph_dict = get_graph_dict(folder)
        save_metrics(foldername, graph_dict, "results/downsampling")
