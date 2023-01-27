import unittest

import networkx as nx
from Population import Population


class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.G = nx.complete_graph(100)
        self.P = Population(self.G)

    def test_population_init(self):
        counts = self.P.count_all()
        self.assertEqual(counts, (90, 5, 5, 0))

    def test_step_all(self):
        self.P.step_all()


if __name__ == "__main__":
    unittest.main()
