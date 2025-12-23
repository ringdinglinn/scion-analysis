import networkx as nx
from metrics.network_partition import calculate_cheeger_costant
from metrics.metrics_basics import calculate_metrics as calculate_basic_metrics
from metrics.spectral import calculate_spectral_metrics
import utils.io as io

def calculate_metrics(G, graph_name):
    metrics = {}
    metrics['graph_index']          = graph_name
    metrics['transitivity']         = nx.transitivity(G)
    print(f"{graph_name}, transitivity: {metrics['transitivity']}")
    metrics['average_clustering']   = nx.average_clustering(G)
    print(f"{graph_name}, average_clustering: {metrics['average_clustering']}")
    metrics['cheeger constant']     = calculate_cheeger_costant(G, 0.45, 3)
    print(f"{graph_name}, cheeger: {metrics['cheeger constant']}")
    metrics['n_spanning_trees']     = nx.number_of_spanning_trees(G)

    try:
        import networkx.algorithms.approximation as nx_app
        metrics['treewidth'] = nx_app.treewidth_min_fill_in(G)[0]
    except:
        metrics['treewidth'] = None

    print(f"{graph_name}, treewidth: {metrics['treewidth']}")
        
    return metrics

def run_all_metrics(graph_list):
    results = []

    for filename, G in graph_list.items():
        if G.number_of_nodes() == 0:
            continue
        basic_metrics = calculate_basic_metrics(G, filename)
        metrics = calculate_metrics(G, filename)
        spectral_metrics = calculate_spectral_metrics(G, filename)

        metrics = basic_metrics | metrics | spectral_metrics

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