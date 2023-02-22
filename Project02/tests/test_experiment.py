import unittest

import networkx as nx
from Experiment import Experiment


class TestExperiment(unittest.TestCase):
    def setUp(self):
        G = nx.circulant_graph(20, [1, 2])
        early_adopters = [1, 2]
        self.E = Experiment(G, 10, 5, "Test", early_adopters)

    def test_run(self):
        expected_result = {
            "time_to_no_change": 0,
            "percentage_adopting": 1.0,
            "clustering_coefficient": 0.5,
            "density": 0.21052631578947367,
            "avg_path_len": 2.8947368421052633,
        }
        result = self.E.run()
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
