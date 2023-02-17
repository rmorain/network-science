import unittest

import networkx as nx
from Experiment import Experiment


class TestExperiment(unittest.TestCase):
    def setUp(self):
        G = nx.circulant_graph(20, [1, 2])
        early_adopters = [1, 2]
        self.E = Experiment(G, 100, 5, "Test", early_adopters)

    def test_run(self):
        self.E.run()


if __name__ == "__main__":
    unittest.main()
