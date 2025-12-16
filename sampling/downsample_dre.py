import networkx as nx
import sys
import os
import numpy as np

def reduce_crve(G, f):
    k = G.number_of_edges() - int(round(G.number_of_edges() * f))
    edges = list(G.edges())
    del_edges = np.random.choice(len(edges), k, replace=False)
    G.remove_edges_from([edges[i] for i in del_edges])
    G.remove_nodes(nx.isolates(G))

if len(sys.argv) < 3:
    print("Usage: python script.py <edgelist_file> <fraction>")
    sys.exit(1)

path = sys.argv[1]
filename = os.path.splitext(os.path.basename(path))[0]
fraction = float(sys.argv[2])

G = nx.read_edgelist(path)
print("Graph loaded successfully!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print(f"Reducing to {fraction}")

reduce_crve(G, fraction)

nx.write_edgelist(G, f"../data/edgelists/{filename}_dre_{str(int(fraction*100))}.txt", data=False)