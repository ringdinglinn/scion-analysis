import networkx as nx
from metrics.network_partition import cheeger_constant
from metrics_basics import calculate_metrics as calculate_basic_metrics
import sys
import utils.io as io

def calculate_metrics(G, graph_name):
    metrics = {}
    metrics['graph_index']          = graph_name
    metrics['transitivity']         = nx.transitivity(G)
    print(f"{graph_name}, transitivity: {metrics['transitivity']}")
    metrics['average_clustering']   = nx.average_clustering(G)
    print(f"{graph_name}, average_clustering: {metrics['average_clustering']}")
    metrics['cheeger constant']     = cheeger_constant(G, 0.45, 3)
    print(f"{graph_name}, cheeger: {metrics['cheeger constant']}")

    try:
        import networkx.algorithms.approximation as nx_app
        metrics['treewidth'] = nx_app.treewidth_min_fill_in(G)[0]
    except:
        metrics['treewidth'] = None

    print(f"{graph_name}, treewidth: {metrics['treewidth']}")

    try:
        metrics['algebraic_connectivity'] = nx.algebraic_connectivity(G)
    except:
        metrics['algebraic_connectivity'] = None
    
    print(f"{graph_name}, algebraic connectivity: {metrics['algebraic_connectivity']}")
    
    return metrics

def run_all_metrics(graph_list):
    results = []

    for filename, G in graph_list.items():
        basic_metrics = calculate_basic_metrics(G, filename)
        metrics = calculate_metrics(G, filename)

        metrics = basic_metrics | metrics

        print(f"Calculated complex metrics for {filename}:\n{metrics}")

        results.append(metrics)

    return results

if __name__ == "__main__":
    user_input = io.user_input_path()
    graphs = {} 
    if io.is_path(user_input):
        graphs = io.load_graphs_from_folder(user_input, directed=False) # double check if this is false
    else:
        graph_name, G = io.load_graph(user_input, directed=False)
        graphs[graph_name] = G

    output_path = io.user_output_path()

    results = run_all_metrics(graphs)
    io.save_metrics_to_csv(results, output_path)