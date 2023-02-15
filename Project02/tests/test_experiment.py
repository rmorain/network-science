import unittest

import networkx as nx
from Experiment import Experiment


class TestExperiment(unittest.TestCase):
    def setUp(self):
        G = nx.complete_graph(100)
        self.E = Experiment(G, 100, 5, "Test")

    def test_run(self):
        self.E.run()


if __name__ == "__main__":
    unittest.main()
