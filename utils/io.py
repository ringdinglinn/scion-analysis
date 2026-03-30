import os
import csv
import networkx as nx
import sys
import json

current_index = 1

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
    global current_index
    if (len(sys.argv) <= current_index) or not (os.path.isfile(sys.argv[current_index]) or is_path(sys.argv[current_index])):
        print("no input path")
        sys.exit(1)

    val = sys.argv[current_index]
    current_index += 1
    return val

def user_input(index=1):
    global current_index
    if (len(sys.argv) <= current_index):
        print("no input path")
        sys.exit(1)

    val = sys.argv[current_index]
    current_index += 1
    return val

def user_output_path(index=None):
    if (index is not None):
        return user_output_path_index(index)
    global current_index
    if (len(sys.argv) <= current_index):
        print("no output path")
        sys.exit(1)

    val = sys.argv[current_index]
    current_index += 1
    return val

def user_output_path_index(index):
    if (len(sys.argv) <= index):
        print("no output path")
        sys.exit(1)
    return sys.argv[index]

def user_input_paths():
    if len(sys.argv) < 2:
        print("need at least one input CSV and one output path")
        sys.exit(1)

    input_paths = sys.argv[1:-1]

    for path in input_paths:
        if not (os.path.isfile(path) or is_path(path)):
            print(f"invalid input path: {path}")
            sys.exit(1)

    return input_paths

def user_output_path_last():
    return user_output_path(index=len(sys.argv) - 1)

def get_filepaths(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def get_filename_from_path(file_path):
    return os.path.basename(file_path)