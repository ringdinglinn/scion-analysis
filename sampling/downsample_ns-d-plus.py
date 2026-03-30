import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
from collections import deque


def counting_sort_by_degree(nodes, G):
    """
    CountingSort for nodes based on degree (descending).
    """
    sorted_nodes = sorted(nodes, key=lambda n: G.degree[n], reverse=True)
    return deque(sorted_nodes)


def NS(phi, node_set):
    """
    Placeholder for NS(φ, node_set). Replace with your sampling method.
    """
    k = int(phi * len(node_set))
    return set(list(node_set)[:k])


def NS_d_plus(phi, G):
    """
    NetworkX implementation of Algorithm NS-d+(φ, N, S, D)
    
    Input:
        phi — sample fraction
        G   — NetworkX graph

    Output: 
        Vs — sampled nodes
        Es — induced edges on sampled nodes
    """

    N = list(G.nodes())
    degrees = np.array([[G.degree[n]] for n in N])

    # Step 2: KMEANS clustering into 3 degree groups
    kmeans = KMeans(n_clusters=3, n_init='auto').fit(degrees)
    labels = kmeans.labels_

    clusters = {0: [], 1: [], 2: []}
    for node, lbl in zip(N, labels):
        clusters[lbl].append(node)

    # Determine which cluster is high, medium, low by avg degree
    avg_deg = {c: np.mean([G.degree[n] for n in clusters[c]]) for c in clusters}
    order = sorted(avg_deg, key=avg_deg.get, reverse=True)

    N_high = clusters[order[0]]
    N_med  = clusters[order[1]]
    N_low  = clusters[order[2]]

    # Step 3: CountingSort on high-degree nodes → Queue
    Q = counting_sort_by_degree(N_high, G)

    # Step 4–5: pick φ * |N_high|
    target = int(phi * len(N_high))
    V_high = set()
    while len(V_high) < target and Q:
        V_high.add(Q.popleft())

    # Step 6–7: medium & low degree using NS(φ, …)
    V_med = NS(phi, N_med)
    V_low = NS(phi, N_low)

    # Step 8: final sample set
    Vs = V_high | V_med | V_low

    # Step 9: deduce sample network (induced edges)
    H = G.subgraph(Vs).copy()
    return H

def load_topology(path, directed=True, sort_nodes=True):
    """
    Load SCION/AS topology file of format:
        provider|customer|type
    Ignores 'type' column and only loads edges.
    """

    G = nx.DiGraph() if directed else nx.Graph()

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            # skip comments & empty lines
            if not line or line.startswith("#"):
                continue

            # parse three columns separated by '|'
            parts = line.split("|")
            if len(parts) != 3:
                continue  # ignore malformed lines

            a, b, relation = parts
            a = a.strip()
            b = b.strip()

            # Add edge
            G.add_edge(a, b)

    # Optional: sort node labels (as strings or ints)
    if sort_nodes:
        sorted_nodes = sorted(G.nodes(), key=lambda x: int(x))
        G = nx.relabel_nodes(G, {old: old for old in sorted_nodes})

    return G


G = load_topology("data/20250901.as-rel.txt")
print(f"Loaded graph, V = {G.number_of_nodes()}, E = {G.number_of_edges()}")
H = NS_d_plus(0.1, G)
print(f"Sampled graph, V = {H.number_of_nodes()}, E = {H.number_of_edges()}")
nx.write_edgelist(H, "CAIDA_250901_ns-d-plus-phi0.1.txt", data=False)

