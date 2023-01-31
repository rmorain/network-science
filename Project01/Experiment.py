import collections

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from Population import Population


class Experiment:
    def __init__(self, G, steps, trials, name):
        self.G = G
        self.name = name
        self.P = Population(self.G)
        self.counts = self.P.count_all()
        self.steps = steps
        self.trials = trials
        self.time_series_data = [
            [
                [],
                [],
                [],
                [],
            ]
            for k in range(self.trials)
        ]

    def run(self):
        for k in range(self.trials):
            counts = self.P.counts
            for i in range(len(counts)):
                self.time_series_data[k][i].append(counts[i])
            for i in range(self.steps):
                self.P.step_all()
                counts = self.P.counts
                for j in range(len(counts)):
                    self.time_series_data[k][j].append(counts[j])
            self.P = Population(self.G)  # Reinitialize population
        self.draw_time_series()
        self.stats()
        self.network_conditions()

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

    def stats(self):
        data = np.array(self.time_series_data).mean(axis=0)
        # Time to peak
        time_to_peak = data[2].argmax()
        print(f"Time to peak: {time_to_peak}")
        # Peak infections
        peak_infections = data[2].max()
        print(f"Peak infections: {peak_infections}")
        # Time until no new infections
        min_sus = data[0].min()
        no_new_infections = np.where(data[0] == min_sus)[0][0]
        print(f"Time to no new infections: {no_new_infections}")
        print(f"Unaffected individuals: {min_sus}")

    def network_conditions(self):
        # Degree distribution
        deg, cnt = self.plot_degree_histogram(self.G, log_scale=False)
        # max degree
        print(f"Max degree: {max(cnt)}")
        # avg degree
        print(f"Avg degree: {np.mean(cnt)}")
        # Diameter
        print(f"Diameter: {nx.diameter(self.G)}")
        # Radius
        print(f"Radius: {nx.radius(self.G)}")
        # Density
        print(f"Density: {nx.density(self.G)}")

    def plot_degree_histogram(self, G, log_scale=False):
        degree_sequence = sorted(
            [d for n, d in G.degree()], reverse=True
        )  # degree sequence
        # print "Degree sequence", degree_sequence
        degreeCount = collections.Counter(degree_sequence)
        deg, cnt = zip(*degreeCount.items())

        fig, ax = plt.subplots()
        plt.bar(deg, cnt, width=0.80, color="b")

        plt.title(f"Degree Histogram of {self.name}")
        plt.ylabel("Count")
        plt.xlabel("Degree")
        ax.set_xticks([d + 0.4 for d in deg])
        ax.set_xticklabels(deg)
        if log_scale:
            plt.xscale("log")
            plt.yscale("log")
            ax.set_aspect("equal", "box")

        plt.show()
        return deg, cnt


if __name__ == "__main__":
    G = nx.barabasi_albert_graph(100, 2)
    E = Experiment(G, 100, 5, "complete graph")
    E.run()
