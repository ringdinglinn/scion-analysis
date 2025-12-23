import random
import networkx as nx
import sys
import os
import utils.io as io

def contract_nodes_in_place(G, u, v):
    # Add edges from v to u
    for neighbor in G.neighbors(v):
        if neighbor != u:  # avoid self-loop
            G.add_edge(u, neighbor)
    G.remove_node(v)

def reduce_crve(G, f):
    k = G.number_of_nodes() - int(round(G.number_of_nodes() * f))
    nodes = list(G.nodes())

    for _ in range(k):
        rand_node = random.choice(nodes)
        rand_neighbor = random.choice(list(G.neighbors(rand_node)))

        contract_nodes_in_place(G, rand_node, rand_neighbor)

        nodes.remove(rand_neighbor)
        G.remove_nodes_from(list(nx.isolates(G)))

if len(sys.argv) < 3:
    print("Usage: python script.py <edgelist_file> <fraction>")
    sys.exit(1)

path = io.user_input_path()
filename = os.path.splitext(os.path.basename(path))[0]

out_path = io.user_output_path(index=2)

fraction = float(io.user_input(index=3))
n = int(io.user_input(index=4))

G = nx.read_edgelist(path)
print("Graph loaded successfully!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print(f"Reducing to {fraction}")

for i in range(n):
    H = G.copy()
    reduce_crve(H, fraction)
    nx.write_edgelist(H, f"{out_path}/{filename}_crve_{str(int(fraction*100))}_{i}.txt", data=False)
    print(f"Saved graph {i+1}/{n}")