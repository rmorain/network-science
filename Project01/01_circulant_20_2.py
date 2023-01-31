import networkx as nx

from Experiment import Experiment

G = nx.circulant_graph(20, [1, 2])
E = Experiment(G, 100, 10, "circulant graph (20, 2)")
E.run()
