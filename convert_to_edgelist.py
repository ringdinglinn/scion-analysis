import networkx as nx
import argparse

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
            parts = line.split("|")
            if len(parts) != 3:
                continue
            a, b, relation = parts
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
    parser = argparse.ArgumentParser(description="Load a SCION/AS topology and export edge list.")
    parser.add_argument("input_file", help="Path to the topology file")
    parser.add_argument("output_file", help="Path to save the edge list")
    args = parser.parse_args()

    G = load_topology(args.input_file, directed=True, sort_nodes=True)
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    nx.write_edgelist(G, args.output_file, data=False)
    print(f"Edge list saved to {args.output_file}")

if __name__ == "__main__":
    main()
