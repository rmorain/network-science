import unittest

import networkx as nx
from Experiment import Experiment
from Graphs import NCM_Graph


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

    def test_ncm_graph(self):
        E = Experiment(NCM_Graph, 1, "Test", [1, 2], 0)
        result = E.run()
        self.assertIsNotNone(result)

    def test_small_world(self):
        G = nx.watts_strogatz_graph(100, 5, 0.3)
        E = Experiment(G, 10, 1, "Test", [7, 8])
        result = E.run()
        self.assertIsNotNone(result)

    def test_connected(self):
        smallWorldGraph_410 = nx.watts_strogatz_graph(410, 3, 0.1)
        assert nx.is_connected(smallWorldGraph_410)


if __name__ == "__main__":
    unittest.main()
