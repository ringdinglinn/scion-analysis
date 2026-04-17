import os
import re
import metrics.network_partition as np
import networkx as nx

cores_dir = "data/20251201/scion_isd/core_edgelists"
isd_dir = "data/20251201/scion_isd/combined_edgelists"
core_file = os.path.join(cores_dir, "20251201.SCION_core_topo.txt")

COUNTRIES = [
    'AU', 'BR', 'CN', 'FR', 'DE', 'IN', 'IR', 'IT',
    'NL', 'RU', 'SG', 'ZA', 'CH', 'UA', 'GB', 'US'
]

def read_edges_and_nodes(path):
    """Return a set of edges (as tuples) and a set of nodes from a file."""
    edges = set()
    nodes = set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            node1, node2 = parts
            edge = tuple(sorted((node1, node2)))
            edges.add(edge)
            nodes.add(node1)
            nodes.add(node2)
    return edges, nodes

total_core_edges, total_core_nodes = read_edges_and_nodes(core_file)
print(f"SCION Core: {len(total_core_nodes)} nodes")

isd_files = {}
pattern_combined = re.compile(r"20251201_scion_isd_(\w+)_combined\.txt")
for f in os.listdir(isd_dir):
    if f.startswith(".") or not f.endswith(".txt"):
        continue
    m = pattern_combined.match(f)
    if m:
        cc = m.group(1)
        isd_files[cc] = os.path.join(isd_dir, f)

pattern_core = re.compile(r"20251201_scion_isd_(\w+)_core\.txt")

results = {}

TOTAL_NODES = 78771

for f in os.listdir(cores_dir):
    if f.startswith(".") or not f.endswith(".txt"):
        continue
    m = pattern_core.match(f)
    if not m:
        continue
    cc = m.group(1)
    if cc not in COUNTRIES:
        continue
    core_path = os.path.join(cores_dir, f)
    isd_path = isd_files.get(cc)
    if isd_path is None:
        print(f"No matching combined file for {f}, skipping.")
        continue


    all_edges_in_isd, all_nodes_in_isd = read_edges_and_nodes(isd_path)

    core_nodes_without_isd = total_core_nodes - all_nodes_in_isd
    
    count_outgoing_edges = sum(
        1
        for n1, n2 in total_core_edges
        if (n1 in core_nodes_without_isd and n2 in all_nodes_in_isd) or (n2 in all_nodes_in_isd and n1 in core_nodes_without_isd)
    )

    core_control = count_outgoing_edges / len(all_nodes_in_isd)

    results[cc] = (count_outgoing_edges, len(all_nodes_in_isd), core_control)
    print(f"{f}: outgoing_edges={count_outgoing_edges}, all_nodes_in_isd={len(all_nodes_in_isd)}")


for cc, (out_edges, n, core_control) in results.items():
    isd_ratio = n / (TOTAL_NODES - n)
    print(f"Calculating cheeger for {cc} with ratio {isd_ratio}")

    isd_path = isd_files.get(cc)
    isd_edges, _ = read_edges_and_nodes(isd_path)

    G = nx.Graph()
    G.add_edges_from(isd_edges)
    res = np.compute(G)
    if res is None:
        results[cc] = (out_edges, n, core_control, isd_ratio, 0,0)
    else:
        cheeger = res
        results[cc] = (out_edges, n, core_control, isd_ratio, cheeger)
        print(f"{cc}, cheeger: {cheeger}, core control: {core_control}, isd ratio: {isd_ratio}")


output_csv = "results/SCION_ISDs_border_breadth.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, "w") as f:
    f.write("cc,out_edges,nodes_in_isd,core_control,isd_ratio,cheeger\n")
    for cc, (out_edges, nodes_in_isd, core_control, isd_ratio, cheeger) in results.items():
        f.write(f"{cc},{out_edges},{nodes_in_isd},{core_control},{isd_ratio},{cheeger}\n")

print(f"Results saved to {output_csv}")
