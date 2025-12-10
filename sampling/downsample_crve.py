import random
import networkx as nx
import sys
import os

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

nx.write_edgelist(G, f"../data/edgelists/{filename}_crve_{str(int(fraction*100))}.txt", data=False)