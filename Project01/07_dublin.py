from Experiment import Experiment
from utils.DublinGraph import DublinGraph

G = DublinGraph._read_graph_from_file()
E = Experiment(G, 100, 10, "Dublin Graph")
E.run()
