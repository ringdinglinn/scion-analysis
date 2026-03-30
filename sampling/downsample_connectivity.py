import networkx as nx
import random
import utils.io as io

def fast_spanning_tree(G):
    root = next(iter(G.nodes))
    T = nx.dfs_tree(G, source=root)
    return set(T.edges())

def connection_downsample(G, k):
    if not nx.is_connected(G):
        raise ValueError("Graph must be connected")

    tree_edges = fast_spanning_tree(G)

    removable = [
        e for e in G.edges()
        if e not in tree_edges and (e[1], e[0]) not in tree_edges
    ]

    if len(removable) < k:
        print("Warning: not enough edges to remove.")
        k = len(removable)

    edges_to_remove = random.sample(removable, k)
    G.remove_edges_from(edges_to_remove)

    return G

def connection_downsample_ratio(G, r):
    k = round(G.number_of_edges() * (1-r))
    return connection_downsample(G, k)

def connection_downsample_avg_deg(G, d):
    k =  G.number_of_edges() - (d * G.number_of_nodes() / 2)
    return connection_downsample(G, int(k))

if __name__ == "__main__":
    user_input = io.user_input_path()
    q = float(io.user_input())
    n = int(io.user_input())
    output_path = io.user_output_path()

    graphs = {} 
    if io.is_path(user_input):
        graphs = io.load_graphs_from_folder(user_input, directed=False) # double check if this is false
    else:
        graph_name, G = io.load_graph(user_input, directed=False)
        graphs[graph_name] = G


    if (q < 1):
        downsample = connection_downsample_ratio
    else:
        downsample = connection_downsample_avg_deg

    for graph_name, G in graphs.items():
        for i in range(n):
            print(f"downsampling {graph_name} to {q}, saving to: {output_path}")
            H = G.copy()
            H = downsample(H, q)
            name = graph_name.split('.')[0]
            io.save_edgelist(H, output_path, f"{name}_conn_{q}_{i}.txt")
        


