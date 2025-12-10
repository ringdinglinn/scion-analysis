"""sparsity"""

import networkx as nx
import itertools
from math import floor
from math import inf

def sparsity(G):
    n = G.number_of_nodes()
    nodes = set(G.nodes())
    q_min = inf

    k = floor(n/2)

    # for k in range(1, floor(n/2) + 1):
    for a in itertools.combinations(nodes, k):
        A = set(a)
        B = nodes - A
        X_A = {u for u in A if any(v in B for v in G.neighbors(u))}
        X_B = {v for v in B if any(u in A for u in G.neighbors(v))}
        q_A = len(X_A) / (len(A-X_A) * len(B)) if len(A-X_A) > 0 else inf
        q_B = len(X_B) / (len(B-X_B) * len(A)) if len(B-X_B) > 0 else inf
        q_min = min(q_A, q_B, q_min)

    return q_min