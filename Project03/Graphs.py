import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from networkx.algorithms.community.centrality import girvan_newman

from AssortativeNetworkManager import MixedNetworkFormation
from Experiment import Experiment


def read_graph_from_file(filename="./ia-infect-dublin/ia-infect-dublin.mtx"):
    fo = open(filename, "r")
    line = fo.readline()  # Read file header
    line = fo.readline()  # Number of vertices and edges
    if not line:
        print("error -- illegal format for input")
        return
    v = line.split(" ")
    numVertices = int(v[0])
    G = nx.Graph()
    G.add_nodes_from(range(1, numVertices + 1))
    while True:
        line = fo.readline()
        if not line:
            break
        # print("Line{}: {}".format(count,line.strip()))
        v = line.split(" ")
        v1 = int(v[0])
        v2 = int(v[1])
        G.add_edge(v1, v2)
        G.add_edge(v2, v1)
    fo.close()
    return G


def _get_graph_nineteenfour_from_NCM_book():
    G = nx.Graph()
    G.add_nodes_from(range(1, 16))
    G.add_edges_from(
        [
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 6),
            (4, 5),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (6, 9),
            (7, 8),
            (7, 9),
            (7, 10),
        ]
    )
    G.add_edges_from(
        [
            (8, 10),
            (8, 14),
            (9, 10),
            (9, 11),
            (10, 12),
            (11, 12),
            (11, 15),
            (12, 13),
            (12, 15),
            (12, 16),
        ]
    )
    G.add_edges_from([(13, 14), (13, 16), (13, 17), (14, 17), (15, 16), (16, 17)])
    return G


def get_nHighestDegreeNodes(G, n):
    degrees = list(G.degree(list(G.nodes)))
    degrees.sort(key=lambda x: x[1], reverse=True)

    return [degrees[i][0] for i in range(n)]


def get_nLowestDegreeNodes(G, n):
    degrees = list(G.degree(list(G.nodes)))
    degrees.sort(key=lambda x: x[1])
    return [degrees[i][0] for i in range(n)]


# Graph from fig 19.4
def NCM_Graph():
    return _get_graph_nineteenfour_from_NCM_book()


# circulant graph with 2 neighbors each side
def circulantGraph_2x():
    return nx.circulant_graph(20, [1, 2])


# circulant graph with 4 neighbors each side
def circulantGraph_4x():
    return nx.circulant_graph(20, [1, 2, 3, 4])


def karateGraph():
    return nx.karate_club_graph()


def BAGraph_100():
    return nx.barabasi_albert_graph(100, 2)


def BAGraph_410():
    return nx.barabasi_albert_graph(410, 2)


def smallWorldGraph_100():
    return nx.watts_strogatz_graph(100, 5, 0.3)


def smallWorldGraph_410():
    return nx.watts_strogatz_graph(410, 3, 0.3)


def dublinGraph():
    return read_graph_from_file()


def assortativeGraph():
    return MixedNetworkFormation(
        color_template=["b", "m", "c", "y", "r", "c", "g"]
    ).getGraph()


def add_random_edges(G, n):
    # Add n random edges to the graph
    count = 0
    while count < n:
        # random edge
        u, v = np.random.choice(np.arange(1, len(G) + 1), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v)
            count += 1
    return G


def random_early_adopters(G, n):
    return np.random.choice(np.arange(1, len(G) + 1), n).tolist()


def eig_centrality_early_adopters(G, n):
    nodes = nx.eigenvector_centrality(G, max_iter=500, tol=1e-2)
    nodes_list = list(nodes.items())
    sorted_nodes_list = sorted(nodes_list, key=lambda x: x[1], reverse=True)
    early_adopters = [x[0] for x in sorted_nodes_list][:n]
    return early_adopters


def add_edges_betweenness(G, n):
    # Add n edges to the graph based on girvan newman betweenness
    betweenness = {}
    # Generate potential edges
    potential_edges = np.random.choice(np.arange(1, len(G) + 1), (100, 2))
    for edge in potential_edges:
        u, v = edge
        # u must be <= v
        if u > v:
            temp = u
            u = v
            v = temp

        if not G.has_edge(u, v):
            G.add_edge(u, v)
            betweenness[(u, v)] = nx.edge_betweenness_centrality(G)[(u, v)]
            G.remove_edge(u, v)
    betweenness_list = list(betweenness.items())
    sorted_betweenness_list = sorted(betweenness_list, key=lambda x: x[1], reverse=True)
    edges_to_add = [x[0] for x in sorted_betweenness_list][:n]
    G.add_edges_from(edges_to_add)
    return G


if __name__ == "__main__":

    Graphs = {
        "assortativeGraph": [
            "random_early_adopters",
            "get_nHighestDegreeNodes",
            "get_nLowestDegreeNodes",
            "eig_centrality_early_adopters",
        ]
        # "NCM_Graph": [[1, 2], [7, 8], [6, 7, 12]],
        # "circulantGraph_2x": [[1, 2], [1, 10]],
        # "circulantGraph_4x": [[1, 2], [1, 2, 3, 4]],
        # "karateGraph": [[1, 2], [33, 34]],
        # "BAGraph_100": [(get_nLowestDegreeNodes, 4), (get_nHighestDegreeNodes, 4)],
        # "BAGraph_410": [(get_nHighestDegreeNodes, 20), (get_nHighestDegreeNodes, 50)],
        # "smallWorldGraph_100": [
        # (get_nLowestDegreeNodes, 4),
        # (get_nHighestDegreeNodes, 4),
        # ],
        # "smallWorldGraph_410": [(get_nHighestDegreeNodes, 20)],
        # "dublinGraph": [(get_nHighestDegreeNodes, 50)],
    }
    trials = 10

    stats_df = pd.DataFrame(
        columns=[
            "name",
            "time_to_no_change",
            "percentage_adopting",
            "clustering_coefficient",
            "density",
            "avg_path_len",
        ]
    )
    graphName = "assortativeGraph"
    graphGenerator = eval(graphName)
    edge_methods = ["add_random_edges", "add_edges_betweenness"]

    for i, earlyAdopters in enumerate(Graphs[graphName]):
        for j, edge_method in enumerate(edge_methods):
            E = Experiment(
                graphGenerator,
                eval(earlyAdopters),
                eval(edge_method),
                trials,
                graphName + "_" + earlyAdopters + "_" + edge_method,
                i,
            )
            stats = E.run()
            stats_df = pd.concat(
                [stats_df, pd.DataFrame(stats, index=[stats_df.shape[0]])]
            )
    stats_df.to_csv("stats_summary.csv")

    y = stats_df["percentage_adopting"].tolist()
    y1 = y[: len(y) // 2]
    y2 = y[len(y) // 2 :]
    X = Graphs[graphName]
    X_axis = np.arange(len(X))
    plt.bar(X_axis - 0.2, y1, 0.4, label="Adding random edges")
    plt.bar(X_axis + 0.2, y2, 0.4, label="Adding edges with high betweenness")
    plt.xticks(X_axis, X)
    plt.title("Percentage Adopting vs. Early Adopters Method")
    plt.ylabel("Percentage Adopting")
    plt.legend()
    plt.savefig("barplot.png")
    plt.show()
