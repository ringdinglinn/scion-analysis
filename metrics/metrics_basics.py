import networkx as nx
import numpy as np
import utils.io as io

def degree_std(G):
    degrees = [d for _, d in G.degree()]
    return np.std(degrees)

def degree_entropy(G):
    degrees = [d for _, d in G.degree()]
    _, counts = np.unique(degrees, return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log2(probs))
    return entropy

def calculate_metrics(G, graph_name):
    metrics = {}
    metrics['graph_index'] = graph_name
    metrics['|V|'] = G.number_of_nodes()
    metrics['|E|'] = G.number_of_edges()
    metrics['avg_degree'] = 2 * G.number_of_edges() / G.number_of_nodes()
    metrics['nr_connected_components'] = nx.number_connected_components(G)
    metrics['degree_std'] = degree_std(G)
    metrics['degree_entropy'] = degree_entropy(G)
    metrics['assortativity'] = nx.degree_assortativity_coefficient(G)

    print(f"Calculated basic metrics for {graph_name}:\n{metrics}")

    return metrics

def run_all_metrics(graph_list):
    results = []

    for filename, G in graph_list.items():
        results.append(calculate_metrics(G, filename))

    return results

if __name__ == "__main__":
    user_input = io.user_input_path()
    graphs = {} 
    if io.is_path(user_input):
        graphs = io.load_graphs_from_folder(user_input, directed=False) # double check if this is false
    else:
        graph_name, G = io.load_graph(user_input, directed=False)
        graphs[graph_name] = G

    output_path = io.user_output_path()

    results = run_all_metrics(graphs)
    io.save_metrics_to_csv(results, output_path)