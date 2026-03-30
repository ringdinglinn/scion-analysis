import random
import networkx as nx
import sys
import os
import utils.io as io


def read_bgp_edgelist(path):
    G = nx.Graph()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(line.strip().split("|"))
            u, v, label, _ = line.strip().split("|")
            G.add_edge(int(u), int(v), label=int(label))
    return G


def write_bgp_edgelist(G, path):
    with open(path, "w") as f:
        for u, v, attrs in G.edges(data=True):
            f.write(f"{u}|{v}|{attrs['label']}|bgp\n")


def contract_nodes_in_place(G, u, v):
    for neighbor, attrs in list(G[v].items()):
        if neighbor == u:
            continue

        if not G.has_edge(u, neighbor):
            G.add_edge(u, neighbor, label=attrs["label"])

    G.remove_node(v)


def reduce_crve(G, f):
    target_removals = G.number_of_nodes() - int(round(G.number_of_nodes() * f))

    for _ in range(target_removals):
        if G.number_of_nodes() <= 1:
            break

        rand_node = random.choice(list(G.nodes()))
        neighbors = list(G.neighbors(rand_node))

        if not neighbors:
            continue

        rand_neighbor = random.choice(neighbors)
        contract_nodes_in_place(G, rand_node, rand_neighbor)

        G.remove_nodes_from(list(nx.isolates(G)))


if len(sys.argv) < 3:
    print("Usage: python script.py <edgelist_file> <fraction>")
    sys.exit(1)


path = io.user_input_path()
filename = os.path.splitext(os.path.basename(path))[0]
out_path = io.user_output_path()

fraction = 0.2
n = 1


G = read_bgp_edgelist(path)
print("Graph loaded successfully!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print(f"Reducing to {fraction}")


for i in range(n):
    H = G.copy()
    reduce_crve(H, fraction)

    write_bgp_edgelist(H, out_path)

    print(f"Saved graph {i + 1}/{n}")
