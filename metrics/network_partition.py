#!/usr/bin/env python3
"""
cheeger_torch.py

PyTorch-based conversion of your partitioning / Cheeger search script.
Uses sparse COO-style tensors (row_idx, col_idx, data) stored as 1-D torch tensors
to avoid densifying large adjacency matrices.

Run:
    python cheeger_torch.py <edgelist_file>

Outputs a JSON file at ../results/cheeger_2.json (create directory if needed).
"""
import sys
import math
import json
import networkx as nx
import torch
import numpy as np
from scipy import sparse as sp
import os
import time

# --- Utilities ----------------------------------------------------------------

def build_sparse_coo_from_nx(G):
    """
    Build COO arrays (row_idx, col_idx, data, shape) from a networkx Graph.
    Returns torch.LongTensor(row_idx), torch.LongTensor(col_idx), torch.FloatTensor(data), shape.
    The adjacency is returned as a (possibly symmetric) COO representation.
    """
    # get scipy coo
    A = nx.to_scipy_sparse_array(G).tocoo()
    row = torch.tensor(A.row, dtype=torch.long)
    col = torch.tensor(A.col, dtype=torch.long)
    data = torch.tensor(A.data, dtype=torch.float32)
    return row, col, data, A.shape

def update_balanced(balanced, assignment, r):
    """
    Updates the balanced tensor in-place.
    - balanced: torch.BoolTensor of shape (n,)
    - assignment: torch.IntTensor of shape (n,) with values ±1
    - r: float, target fraction
    """
    n = assignment.numel()
    num_neg = (assignment == -1).sum().item()
    num_pos = n - num_neg

    a = num_neg + assignment
    b = num_pos - assignment
    s = torch.minimum(a, b)

    max_m = round(n * 0.05)
    s_r = round(min(n * r, n * (1 - r)))

    # in-place update
    balanced.copy_(torch.abs(s_r - s) <= max_m)

# --- Sparse helpers -----------------------------------------------------------

def compute_cut_data_from_adj(adj_row, adj_col, adj_data, assignment):
    """
    Given adjacency in COO (adj_row, adj_col, adj_data) and assignment (tensor of ±1),
    compute cut_matrix = adj @ diag(assignment) in COO-value form.
    For each nonzero (i,j) of adj, cut_value = adj_value * assignment[j].
    Returns cut_row, cut_col, cut_data (same indices as adjacency with new values).
    (We simply reuse adj_row/adj_col and modify data.)
    """
    # assignment is 1-D tensor (n,), and adj_col indexes into it
    cut_data = adj_data * assignment[adj_col].to(adj_data.dtype)
    return adj_row, adj_col, cut_data

def row_sum_from_coo(row_idx, values, n_rows, dtype=torch.float32):
    """
    Given COO (row_idx, values), compute row-wise sum vector of length n_rows.
    Uses scatter_add.
    """
    row_sums = torch.zeros(n_rows, dtype=values.dtype)
    row_sums = row_sums.scatter_add(0, row_idx, values)
    return row_sums

def count_neg_entries_in_DX(row_idx, col_idx, cut_data, assignment):
    """
    Compute D @ cut_matrix values for each nonzero entry: value2 = assignment[row]*cut_data
    Count how many of those are equal to -1 (exact equality, same semantics as original).
    Returns integer count.
    """
    v2 = assignment[row_idx].to(cut_data.dtype) * cut_data
    # equality with -1 (use elementwise comparison)
    return int((v2 == -1).sum().item())

# --- Algorithm ---------------------------------------------------------------

def partition_pass(G, r):
    """
    One pass of the partition improvement heuristic, implemented with PyTorch tensors.
    Returns tuple (min_cuts, |A|, |B|) found during this pass (same semantics as original).
    """
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return None

    # Mapping from node label -> contiguous index [0..n-1]
    idx_of_node = {node: i for i, node in enumerate(nodes)}
    # Build adjacency as COO via scipy then to torch
    adj_sp = nx.to_scipy_sparse_array(G).tocoo()
    # Sanity: if adjacency has shape mismatch, handle it
    assert adj_sp.shape[0] == n and adj_sp.shape[1] == n, "Adjacency shape mismatch with node list"

    adj_row = torch.tensor(adj_sp.row, dtype=torch.long)
    adj_col = torch.tensor(adj_sp.col, dtype=torch.long)
    adj_data = torch.tensor(adj_sp.data, dtype=torch.float32)

    # initial random partition: choose k nodes for A (assignment -1), rest 1
    k = round(n * r)
    perm = torch.randperm(n)
    A_idx = perm[:k]

    assignment = torch.ones(n, dtype=torch.int32)
    assignment[A_idx] = -1

    moveable = torch.ones(n, dtype=torch.bool)

    # Compute cut_matrix = adj @ diag(assignment) in COO form
    cut_row, cut_col, cut_data = compute_cut_data_from_adj(adj_row, adj_col, adj_data, assignment)

    # balanced per vertex
    balanced = torch.ones(n, dtype=torch.bool)
    update_balanced(balanced, assignment, r)

    cuts = []

    # To avoid infinite loop, make sure we stop if no candidate exists
    while (moveable & balanced).any().item():
        # Compute gains:
        # gains = - (D @ cut_matrix).sum(axis=1)
        # D @ cut_matrix multiplies each row by assignment[row], so
        # rowwise_sum = sum_j cut_data[row, j]
        row_sums = row_sum_from_coo(cut_row, cut_data, n)            # sum_j cut_data[row, j]
        # D multiplies row_sums by assignment
        gains = - (assignment.to(row_sums.dtype) * row_sums)        # shape (n,)

        # Find candidate indices where moveable & balanced
        candidates = torch.where(moveable & balanced)[0]
        if candidates.numel() == 0:
            break

        candidate_vals = gains[candidates]
        # choose the candidate with maximum gain (ties broken arbitrarily)
        max_idx_in_candidates = torch.argmax(candidate_vals)
        max_vertex = int(candidates[max_idx_in_candidates].item())

        # flip assignment for that vertex
        assignment[max_vertex] *= -1

        # Update cut_data: because cut_data = adj_value * assignment[col]
        # flipping assignment[v] toggles sign of all entries with col == v
        affected = (cut_col == max_vertex)
        if affected.any().item():
            cut_data[affected] *= -1

        # Update balanced after flip
        update_balanced(balanced, assignment, r)

        # Count cuts: number of entries in D @ cut_matrix equal to -1, divide by 2
        n_cuts_raw = count_neg_entries_in_DX(cut_row, cut_col, cut_data, assignment)
        n_cuts = n_cuts_raw // 2

        cuts.append((n_cuts,
                     int((assignment == -1).sum().item()),
                     int((assignment == 1).sum().item())))

        # mark vertex as non-moveable
        moveable[max_vertex] = False

    return min(cuts, key=lambda x: x[0]) if cuts else None

# --- Top-level helpers -------------------------------------------------------

def cheeger(c, a, b):
    return c / min(a, b)

def run_passes(G, r, n_passes):
    min_cheeger = math.inf
    updates = 0
    min_partition = None

    for i in range(n_passes):
        res = partition_pass(G, r)
        if res is None:
            print(f"pass {i}: no improving moves (empty or trivial partition).")
            continue
        c, a, b = res

        current = cheeger(c, a, b)
        if current < min_cheeger:
            min_cheeger = current
            updates += 1
            min_partition = (c, a, b)

        print(f"pass: {i}, updates: {updates}, cur_cheeger: {current:.6f}")

    return min_partition

# --- JSON encoder for torch types -------------------------------------------

class TorchJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if torch.is_tensor(obj):
            return obj.tolist()
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        return super().default(obj)

# --- main --------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python cheeger_torch.py <edgelist_file>")
        sys.exit(1)

    path = sys.argv[1]
    G = nx.read_edgelist(path)

    # Example r values; you had only 0.45 earlier
    r_s = [0.45]
    results = {}
    for r in r_s:
        start = time.time()
        res = run_passes(G, r, 5)
        elapsed = time.time() - start
        if res is None:
            results[str(r)] = None
        else:
            c, a, b = res
            results[str(r)] = {"cheeger": cheeger(c, a, b), "c": c, "a": a, "b": b}
        print(f"r={r}: {elapsed:.2f}s")

    # ensure results directory exists (relative)
    out_dir = os.path.join("..", "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cheeger_2.json")

    with open(out_path, "w") as f:
        json.dump(results, f, indent=4, cls=TorchJSONEncoder)

    print(f"Done — results written to: {out_path}")

if __name__ == "__main__":
    main()
