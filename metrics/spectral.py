import networkx as nx
import numpy as np
import utils.io as io
from scipy import sparse

def natural_connectivity(G, e):
    return np.log(np.sum(np.exp(e)) / G.number_of_nodes())

def spectral_gap(e):
    return e[0] - e[1]

def spectral_radius(e):
    return e[0]

def effective_resistance(e, n):
    min_rg = n/e[1]
    max_rg = n*(n-1)/e[1]
    rg = n * np.sum(1/e[1:])
    n_rg = (rg - min_rg) / (max_rg - min_rg)
    return rg, min_rg, max_rg, n_rg

def NSC(e):
    return np.sum(np.sinh(e))

def A(e0):
    return np.sinh(e0)**(-0.5)

def spectral_scaling(e_vals, e_vecs):
    sum = 0
    n = len(e_vecs[0])
    for i in range(n):
        observed = np.log(e_vecs[0][i])
        print(f"observed = {observed}")
        logA = np.log(A(e_vals[0]))
        print(f"logA = {logA}")
        logNSC = 0.5 * np.log(NSC(e_vals))
        print(f"logNSC = {logNSC}")
        predicted = logA + logNSC
        sum +=  (observed - predicted)**2
    
    return np.sqrt(sum / float(n))

def calculate_spectral_metrics(G, graph_name):
    metrics = {}
    metrics["graph_index"] = graph_name

    A = sparse.coo_matrix(nx.adjacency_matrix(G))
    n = A.shape[0]
    e_vals, e_vecs = sparse.linalg.eigsh(A, k=min(n-1, 10), which='LA')
    pairs = list(zip(e_vals, e_vecs.T))
    pairs.sort(key=lambda x: x[0], reverse=True)
    e_vals = np.array([p[0] for p in pairs])
    e_vecs = np.column_stack([p[1] for p in pairs])
    print(e_vals)
    metrics["natural connectivity"] = natural_connectivity(G, e_vals)
    metrics["spectral gap"] = spectral_gap(e_vals)
    metrics["spectral radius"] = spectral_radius(e_vals)
    # metrics["spectral scaling"] = spectral_scaling(e_vals, e_vecs)

    L = sparse.coo_matrix(nx.laplacian_matrix(G))
    k = min(n-1, 10)
    e_, _ = sparse.linalg.eigsh(L, k=k, which='SM')
    e_ = np.sort(e_)
    print(e_)
    rg, min_rg, max_rg, n_rg = effective_resistance(e_, G.number_of_nodes())

    metrics["effective graph resistance"] = rg
    metrics["min effective graph resistance"] = min_rg
    metrics["max effective graph resistance"] = max_rg
    metrics["normalized effective graph resistance"] = n_rg
    
    metrics["algebaric connectivity"] = e_[1]

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