import utils.io as io
import networkx as nx
import matplotlib.pyplot as plt


SCION_TESTBED_EDGELIST = "data/scion-testbed.txt"

_, G = io.load_graph(SCION_TESTBED_EDGELIST)

print(G.nodes())


pos = nx.spring_layout(G, seed=42)
FIGSIZE = (8, 8)

fig, ax = plt.subplots(figsize=FIGSIZE)

nx.draw(G, with_labels = True, node_color="orange")

ax.set_axis_off()
plt.tight_layout()
plt.savefig("plots/imgs/scion_testbed_graph.pdf", dpi=300)
plt.close(fig)