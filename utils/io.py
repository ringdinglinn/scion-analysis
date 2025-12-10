import os
import csv
import networkx as nx
import sys

def load_graphs_from_folder(folder_path, directed=True):
    graphs = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            _, G = load_graph(file_path, directed=directed)
            graphs[filename] = G
            print(f"Loaded {filename} with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return graphs

def load_graph(file_path, directed = False):
    filename = os.path.basename(file_path)
    if directed:
        G = nx.read_edgelist(file_path, create_using=nx.DiGraph())
    else:
        G = nx.read_edgelist(file_path, create_using=nx.Graph())

    return filename, G

def load_csv(path):
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def is_path(string):
    return os.path.isdir(string)

def save_metrics_to_csv(metrics_list, output_file):
    if not metrics_list:
        print("No metrics to save.")
        return

    headers = list(metrics_list[0].keys())
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for metrics in metrics_list:
            writer.writerow(metrics)
    print(f"Metrics saved to {output_file}")

def user_input_path():
    if (len(sys.argv) < 2):
        print("no input path")
        sys.exit(1)

    return sys.argv[1]

def user_output_path():
    if (len(sys.argv) < 3):
        print("no output path")
        sys.exit(1)

    return sys.argv[2]