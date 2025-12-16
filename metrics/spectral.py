import networkx as nx
import numpy as np
import utils.io as io

def eigenvals(M):
    e = np.linalg.eigvals(M.toarray())
    e = e.real
    e = np.sort(e)[::-1]
    return e

def natural_connectivity(G, e):
    return np.log(np.sum(np.exp(e)) / G.number_of_nodes())

def spectral_gap(e):
    return e[0] - e[1]

def spectral_radius(e):
    return e[0]

def network_criticality(e, n):
    return np.sum(1/e[1:])/n

def calculate_spectral_metrics(G, graph_name):
    metrics = {}
    metrics["graph_index"] = graph_name
    A = nx.adjacency_matrix(G)
    e = eigenvals(A)
    metrics["natural connectivity"] = natural_connectivity(G, e)
    metrics["spectral gap"] = spectral_gap(e)
    metrics["spectral radius"] = spectral_radius(e)

    L = nx.normalized_laplacian_matrix(G)
    e_ = eigenvals(L)
    metrics["effective graph resistance"] = network_criticality(e_, G.number_of_nodes())
    metrics["algebaric connectivity"] = nx.algebraic_connectivity(G)

    return metrics

if __name__ == "__main__":
    user_input = io.user_input_path()
    graphs = {} 
    if io.is_path(user_input):
        graphs = io.load_graphs_from_folder(user_input, directed=False)
    else:
        graph_name, G = io.load_graph(user_input, directed=False)
        graphs[graph_name] = G

    output_path = io.user_output_path()

    results = [calculate_spectral_metrics(name, G) for name, G in graphs.items()]  

    io.save_metrics_to_csv(results, output_path)