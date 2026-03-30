import utils.io as io
import networkx as nx

n = int(io.user_input())
v = int(io.user_input())
d = int(io.user_input())

output_path = io.user_output_path()

for i in range(n):
    G = nx.random_regular_expander_graph(v, d, max_tries=10000000)
    io.save_edgelist(G, output_path, f"expander_graph_{i}.txt")
