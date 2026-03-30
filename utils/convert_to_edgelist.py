import networkx as nx
import argparse
import utils.io as io

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
            if not line or line.startswith("#"):
                continue

            print(line)
            parts = line.split("|")
            a, b = parts[0], parts[1]
            a = a.strip()
            b = b.strip()
            G.add_edge(a, b)

    if sort_nodes:
        try:
            sorted_nodes = sorted(G.nodes(), key=lambda x: int(x))
        except ValueError:
            sorted_nodes = sorted(G.nodes())
        G = nx.relabel_nodes(G, {old: old for old in sorted_nodes})

    return G

def main():
    user_input = io.user_input_path()
    files = {}
    if io.is_path(user_input):
        paths = io.get_filepaths(user_input)
    else:
        paths = [user_input]

    for path in paths:
        files[path] = load_topology(path, directed=False)

    output_path = io.user_output_path()

    for path, G in files.items():
        name = io.get_filename_from_path(path)
        nx.write_edgelist(G, f"{output_path}/{name}" , data=False)

        print(f"Edge list saved to {output_path}/{name}")

if __name__ == "__main__":
    main()
