import os
import sys
import networkx as nx


def read_routing_file(path, G, directed=False):
    with open(path) as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Skip metadata lines (e.g. destination ASN)
            if "|" not in line:
                continue

            try:
                u, v = line.split("|", 1)
                u = int(u)
                v = int(v)
            except ValueError:
                continue

            G.add_edge(u, v)


def merge_directory(input_dir, directed=False):
    G = nx.DiGraph() if directed else nx.Graph()

    for filename in os.listdir(input_dir):
        path = os.path.join(input_dir, filename)

        if not os.path.isfile(path):
            continue

        read_routing_file(path, G, directed)

    return G


if len(sys.argv) != 3:
    print("Usage: python merge_routing_topos.py <input_dir> <output_file>")
    sys.exit(1)

input_dir = sys.argv[1]
output_file = sys.argv[2]

G = merge_directory(input_dir, directed=True)

print(f"Merged graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

nx.write_edgelist(G, output_file, data=False)
print(f"Saved merged edge list to {output_file}")
