import networkit as nk

# Load graph
reader = nk.graphio.EdgeListReader('|', 1, commentPrefix = '#', continuous = False, directed = False) 
G = reader.read("data/CAIDA_20250901_sorted.txt")

# ---- Heavy-edge matching (weighted case) ----
matcher = nk.matching.SuitorMatcher(G)
matcher.run()
M = matcher.getMatching()

# ---- Coarsen graph ----
coarse = nk.coarsening.MatchingCoarsening(G, M)
coarse.run()

G_coarse = coarse.getCoarseGraph()

print("Original nodes:", G.numberOfNodes())
print("Coarse nodes:", G_coarse.numberOfNodes())