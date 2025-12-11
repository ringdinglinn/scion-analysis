import Graph_Sampling as gs
import networkx as nx
import utils.io as io
import random

def sample(G, ratio):
    print(f"Sampling graph, |V| = {len(G.nodes)}")
    
    sampler = gs.MHRW()
    k = round(G.number_of_nodes() * ratio)
    
    # pick seed with non-zero degree
    non_zero_nodes = [n for n in G.nodes if G.degree[n] > 0]
    if not non_zero_nodes:
        raise ValueError("Graph has no nodes with non-zero degree")
    seed = random.choice(non_zero_nodes)
    
    # run MHRW
    H = sampler.mhrw(G, seed, k)
    return H

if __name__ == "__main__":
    user_input = io.user_input_path()
    graphs = {} 
    if io.is_path(user_input):
        graphs = io.load_graphs_from_folder(user_input, directed=False)
    else:
        graph_name, G = io.load_graph(user_input, directed=False)
        graphs[graph_name] = G

    output_path = io.user_output_path()

    ratios = [0.2]

    for name, G in graphs.items():
        for ratio in ratios:
            G = sample(G, ratio)
            io.save_edgelist(G, output_path, f"{name}_mhrw_{ratio}.txt")
