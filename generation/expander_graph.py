import utils.io as io
import networkx as nx

n = int(io.user_input())
v = int(io.user_input(index=2))
d = int(io.user_input(index=3))

output_path = io.user_output_path(index=4)

for i in range(n):
    G = nx.random_regular_expander_graph(v, d, max_tries=100000000)
    io.save_edgelist(G, output_path, f"expander_graph_{i}.txt")
