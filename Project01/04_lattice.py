import networkx as nx

from Experiment import Experiment

G = nx.grid_2d_graph(10, 10)
E = Experiment(G, 100, 10, "lattice graph")
E.run()
