import networkx as nx

from Experiment import Experiment

G = nx.complete_graph(100)
E = Experiment(G, 100, 10, "complete graph")
E.run()
