import Graph_Sampling as gs
import networkx as nx
import utils.io as io
import random

def sample_SRW(G, ratio):
    sampler = gs.SRW_RWF_ISRW()
    k = round(G.number_of_nodes() * ratio)
    return sampler.random_walk_sampling_simple(G, k)

def sample_with_seed(G, ratio, sampler_class, method_name):
    sampler = sampler_class()
    k = round(G.number_of_nodes() * ratio)
    
    non_zero_nodes = [n for n in G.nodes if G.degree[n] > 0]
    if not non_zero_nodes:
        raise ValueError("Graph has no nodes with non-zero degree")
    seed = random.choice(non_zero_nodes)
    
    method = getattr(sampler, method_name)
    H = method(G, seed, k)
    return H

def sample_mhrw(G, ratio):
    return sample_with_seed(G, ratio, gs.MHRW, 'mhrw')

def sample_RWF(G, ratio):
    sampler = gs.SRW_RWF_ISRW()
    k = round(G.number_of_nodes() * ratio)
    return sampler.random_walk_sampling_with_fly_back(G, k, 0.5)

def sample_ISRW(G, ratio):
    sampler = gs.SRW_RWF_ISRW()
    k = round(G.number_of_nodes() * ratio)
    return sampler.random_walk_induced_graph_sampling(G, k)

def sample_SB(G, ratio):
    sampler = gs.Snowball()
    n = round(G.number_of_nodes() * ratio)
    return sampler.snowball(G, n, 4)

def sample_FF(G, ratio):
    sampler = gs.ForestFire()
    return sampler.forestfire(G, round(G.number_of_nodes() * ratio))

def sample_TIES(G, ratio):
    sampler = gs.TIES()
    k = round(G.number_of_nodes() * ratio)
    return sampler.ties(G, k, 3*k/4)

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
            for method_name, method_func in [
                # ("mhrw", sample_mhrw),
                # ("rwf", sample_RWF),
                # ("isrw", sample_ISRW),
                # ("sb", sample_SB),
                # ("ff", sample_FF),
                # ("srw", sample_SRW),
                ("ties", sample_TIES),
            ]:
                H = method_func(G, ratio)
                name = name.rsplit('.', 1)[0]
                io.save_edgelist(H, output_path, f"{name}_{method_name}_{ratio}.txt")
                print(f"Saved: {name}_{method_name}_{ratio}.txt")
