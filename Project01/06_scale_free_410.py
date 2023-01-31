import networkx as nx

from Experiment import Experiment

G = nx.barabasi_albert_graph(410, 3)
E = Experiment(G, 100, 10, "Scale-free")
E.run()
