import os
import csv
import networkx as nx
import sys
import json

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

def save_json(data, out_path):
    with open(out_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Done — results written to: {out_path}")

def save_edgelist(G, path, name):
    nx.write_edgelist(G, os.path.join(path, name))

def user_input_path(index=1):
    if (len(sys.argv) < index+1) or not (os.path.isfile(sys.argv[index]) or is_path(sys.argv[index])):
        print("no input path")
        sys.exit(1)

    return sys.argv[index]

def user_input(index=1):
    if (len(sys.argv) < index+1):
        print("no input path")
        sys.exit(1)

    return sys.argv[index]

def user_output_path(index=2):
    if (len(sys.argv) < index+1):
        print("no output path")
        sys.exit(1)

    return sys.argv[index]