import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import iqr

sns.set()

from Population import Population


class Experiment:
    def __init__(self, G, name):
        self.G = G
        self.name = name
        self.P = Population(self.G)
        self.counts = self.P.count_all()
        self.steps = 100
        self.trials = 5
        self.time_series_data = [
            [
                [self.P.counts[0]],
                [self.P.counts[1]],
                [self.P.counts[2]],
                [self.P.counts[3]],
            ]
            for k in range(self.trials)
        ]

    def run(self):
        for k in range(self.trials):
            for i in range(self.steps):
                self.P.step_all()
                counts = self.P.counts
                for i in range(len(counts)):
                    self.time_series_data[k][i].append(counts[i])
        self.draw_time_series()

    def draw_time_series(self):
        data = np.array(self.time_series_data)
        mean_data = data.mean(axis=0)
        Q1 = np.quantile(data, 0.25, axis=0)
        Q3 = np.quantile(data, 0.75, axis=0)
        x = list(range(self.steps + 1))
        plt.plot(x, mean_data[0], label="S")
        plt.plot(x, mean_data[1], label="E")
        plt.plot(x, mean_data[2], label="I")
        plt.plot(x, mean_data[3], label="R")
        plt.fill_between(x, Q1[0], Q3[0], alpha=0.3)
        plt.fill_between(x, Q1[1], Q3[1], alpha=0.3)
        plt.fill_between(x, Q1[2], Q3[2], alpha=0.3)
        plt.fill_between(x, Q1[3], Q3[3], alpha=0.3)
        plt.xlabel("Timestep")
        plt.ylabel("# of individuals")
        plt.legend()
        plt.title(f"SEIR Model for {self.name} {len(self.G)} nodes")
        plt.show()


if __name__ == "__main__":
    G = nx.complete_graph(100)
    E = Experiment(G, "complete graph")
    E.run()
