import networkx as nx
import sys
import os
import random
import utils.io as io

def reduce_dre(G, d):
    k = round(G.number_of_edges() - d * G.number_of_nodes() / 2)
    print(f"Deleting {k} edges.")
    edges = list(G.edges())
    del_edges = random.sample(edges, round(k*0.9))
    G.remove_edges_from(del_edges)
    G.remove_nodes_from(list(nx.isolates(G)))
    while abs((G.number_of_edges() * 2 / G.number_of_nodes()) - d) > 0.1:
        del_edges = random.sample(list(G.edges()), 1)
        G.remove_edges_from(del_edges)
        G.remove_nodes_from(list(nx.isolates(G)))

    return G

if len(sys.argv) < 3:
    print("Usage: python script.py <edgelist_file> <fraction>")
    sys.exit(1)

path = io.user_input_path()
filename = os.path.splitext(os.path.basename(path))[0]
q = float(io.user_input())
n = int(io.user_input())
output = io.user_output_path()

G = nx.read_edgelist(path)
print("Graph loaded successfully!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print(f"Reducing to {q}")

for i in range(n):
    H = G.copy()
    reduce_dre(H, q)
    io.save_edgelist(H, output, f"{filename}_dre_{str(q)}_{i}.txt")