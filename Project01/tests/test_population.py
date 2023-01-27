import unittest

import networkx as nx
from Agent import Agent
from Population import Population


class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.G = nx.complete_graph(100)
        self.P = Population(self.G)

    def test_population_init(self):
        counts = self.P.count_all()
        self.assertEqual(counts, (90, 5, 5, 0))
        neighbors = [n for n in self.P.population[0].neighbors]
        self.assertEqual(type(neighbors[0]), Agent)

    def test_step_all(self):
        self.P.step_all()


if __name__ == "__main__":
    unittest.main()
