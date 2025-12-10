import networkx as nx
import random
import numpy as np
import sys
import math
import json
from scipy import sparse

# def is_balanced(assignment, base_vertex, r):
#     base_vert_ass = assignment[base_vertex]
#     n = len(assignment)
#     a = np.sum(assignment == -1) + base_vert_ass
#     b = n - a - base_vert_ass
#     s = min(a, b)

#     max_m = round(n * 0.05)
#     s_r = round(min(n * r, n * (1-r)))
#     return abs(s_r - s) <= max_m

def is_balanced(assignment, balanced, r):
    n = assignment.shape[0]

    num_neg = np.sum(assignment == -1)
    num_pos = n - num_neg

    a = num_neg + assignment
    b = num_pos - assignment
    s = np.minimum(a, b)

    max_m = round(n * 0.05)
    s_r = round(min(n*r, n*(1-r)))

    balanced = np.abs(s_r - s) <= max_m 
    return balanced

def unique_column_counts(A):
    A = A.tocsc()
    n_rows = A.shape[0]
    counts = np.zeros(A.shape[1], dtype=int)

    for j in range(A.shape[1]):
        col_data = A.data[A.indptr[j] : A.indptr[j+1]]
        uniques = set(col_data)
        if len(col_data) < n_rows:  # add zero if column not fully stored
            uniques.add(0)
        counts[j] = len(uniques)

    unique_vals, occurrences = np.unique(counts, return_counts=True)
    print(f"unique column counts: {unique_vals, occurrences}")

def collapse_columns(A):
    A = A.tocsc()  # CSC for fast column access
    n_cols = A.shape[1]
    result = np.zeros(n_cols, dtype=A.dtype)

    for j in range(n_cols):
        col_data = A.data[A.indptr[j] : A.indptr[j+1]]  # nonzero values
        if len(col_data) > 0:
            result[j] = col_data[0]  # pick any nonzero entry
        else:
            result[j] = 0  # or np.nan if you prefer

    return result

def matrix_sanity_check(assignment, cut_mat):
    return np.array_equal(assignment, collapse_columns(cut_mat))


def partition_pass(G, r):
    nodes = np.array(list(G.nodes()))
    n = len(nodes)
    k = round(n * r)
    adj_matrix = nx.to_scipy_sparse_array(G)

    A = np.random.choice(nodes, k, replace=False)
    assignment = np.array([-1 if v in A else 1 for v in nodes])
    
    # print(f"|A| = {np.sum(assignment == -1)}, |B| = {np.sum(assignment == 1)}")

    moveable = np.array([True for _ in nodes])
    cuts = []
    cut_matrix = adj_matrix.copy()
    cut_matrix = cut_matrix @ sparse.diags(assignment)

    balanced = np.array([is_balanced(assignment, v, r) for v in range(len(assignment))])
    # balanced = is_balanced(assignment, balanced, r)

    row_idx = np.repeat(np.arange(n), np.diff(cut_matrix.indptr))
    col_idx = cut_matrix.indices

    while np.any(moveable & balanced):
        # print(f"sanity check pass: {matrix_sanity_check(assignment, cut_matrix)}")
        # print("total: ", np.sum(moveable & balanced))
        gains = (-(sparse.diags(assignment) @ cut_matrix)).sum(axis=1)
        gains = np.array(gains).flatten()
        indices = np.arange(n)
        idx_gains = np.stack((indices, gains), axis=1)

        max_vertex, max_gain = max(idx_gains[moveable & balanced], key=lambda x: x[1])
        max_vertex = int(max_vertex)
        
        # print(f"max vertex: {max_vertex}, max gain: {max_gain}, max vertex degree: {G.degree[nodes[max_vertex]]}")
        # print(f"max vert row: {np.unique(cut_matrix[[max_vertex]].toarray().ravel(), return_counts=True)}, {np.sum(cut_matrix[[max_vertex]].toarray().ravel())}, {gains[max_vertex]}")
        # print(f"base: {max_vertex}")

        moveable[max_vertex] = False
        affected = col_idx == max_vertex
        cut_matrix.data[affected] *= -1
        assignment[max_vertex] *= -1
        
        # balanced = np.array([is_balanced(assignment, v, r) for v in range(len(assignment))])
        balanced = is_balanced(assignment, balanced, r)

        n_cuts = np.sum((sparse.diags(assignment) @ cut_matrix).data == -1)
        n_cuts = round(n_cuts/2)
        cuts.append((n_cuts, np.sum(assignment == -1), np.sum(assignment == 1)))

    c, a, b = min(cuts, key=lambda x: x[0])
    print(f"cuts: {c}, |A| = {a}, |B| = {b}")
    return min(cuts, key=lambda x: x[0]) if cuts else None

def cheeger(c, a, b):
    return c / min(a, b)

def run_passes(G, r, n):
    min_cheeger = math.inf
    updates = 0

    min_partition = None

    for i in range(n):
        c, a, b = partition_pass(G, r)

        if (cheeger(c, a, b) < min_cheeger):
            min_cheeger = cheeger(c, a, b)
            updates += 1
            min_partition = (c, a, b)

        print(f"pass: {i}, updates: {updates}")

    return min_partition

def cheeger_constant(G, r, n):
    c, a, b = run_passes(G, r, n)
    return cheeger(c, a, b)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)
    
def main():

    if len(sys.argv) < 2:
        print("Usage: python script.py <edgelist_file>")
        sys.exit(1)

    path = sys.argv[1]
    G = nx.read_edgelist(path)

    # r_s = [0.06, 0.15, 0.25, 0.35, 0.45]
    r_s = [0.45]
    results = {}
    for r in r_s:
        c, a, b = run_passes(G, r, 5)
        results[str(r)] = (cheeger(c, a, b), c, a, b)

    with open("../results/cheeger_2.json", "w") as f:
        json.dump(results, f, indent=4, cls=NumpyEncoder)

if __name__ == "__main__":
    main()