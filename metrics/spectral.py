import networkx as nx
import numpy as np
import utils.io as io

def eigenvals(M):
    e = np.linalg.eigvals(M.toarray())
    e = e.real
    e = np.sort(e)[::-1]
    return e

def natural_connectivity(e):
    return np.log(np.sum(np.exp(e)) / G.number_of_nodes())

def spectral_gap(e):
    return e[0] - e[1]

def spectral_radius(e):
    return e[0]

def network_criticality(e, n):
    return np.sum(1 / e[1:])/n

def spectral_metrics(G):
    metrics = {}
    A = nx.adjacency_matrix(G)
    e = eigenvals(A)
    metrics["natural connectivity"] = natural_connectivity(e)
    metrics["spectral gap"] = spectral_gap(e)
    metrics["spectral radius"] = spectral_radius(e)

    L = nx.laplacian_matrix(G)
    e_ = eigenvals(L)
    metrics["effective graph resistance"] = network_criticality(e_, G.number_of_nodes())

    return metrics

def spectral_gap(G):

if __name__ == "__main__":
    user_input = io.user_input_path()
    graphs = {} 
    if io.is_path(user_input):
        graphs = io.load_graphs_from_folder(user_input, directed=False)
    else:
        graph_name, G = io.load_graph(user_input, directed=False)
        graphs[graph_name] = G

    output_path = io.user_output_path()

    results = {name: natural_connectivity(g) for name, g in graphs.items()}

    io.save_json(results, output_path)