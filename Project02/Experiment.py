import collections

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import tabulate

from Population import Population
from State import State


class Experiment:
    def __init__(self, graphGenerator, steps, trials, name, early_adopters):
        self.graphGenerator = graphGenerator
        self.name = name
        self.early_adopters = early_adopters

        self.steps = steps
        self.trials = trials
        self.time_series_data = [[] for k in range(self.trials)]

    def run(self):
        for k in range(self.trials):
            self.G = self.graphGenerator()
            mapping = {
                n: i
                for (n, i) in zip(self.G.nodes(), range(1, len(self.G.nodes()) + 1))
            }
            nx.relabel_nodes(self.G, mapping, False)

            if not isinstance(self.early_adopters, list):
                self.early_adopters = self.early_adopters[0](
                    self.G, self.early_adopters[1]
                )

            self.P = Population(self.G, self.early_adopters)

            self.time_series_data[k].append(self.P.counts[State.STATE_A])
            if len(self.G) < 100:
                self.draw = True
            else:
                self.draw = False

            if self.draw and k == 0:
                self.animateGraph(False, 0)

            for i in range(self.steps):
                self.P.step_all()

                if self.draw and k == 0:
                    self.animateGraph(False, i + 1)

                self.time_series_data[k].append(self.P.counts[State.STATE_A])
        self.draw_time_series()
        return self.stats()

    def animateGraph(self, draw_only_nodes, step):
        plt.clf()
        plt.figure(1)
        plt.ion()
        node_color = [agent.current_state.value for agent in self.P.population.values()]

        if draw_only_nodes:
            animate = nx.draw_networkx_nodes
        else:
            animate = nx.draw

        animate(
            self.G,
            pos=nx.nx_agraph.graphviz_layout(self.G, prog="neato"),
            node_size=15,
            node_color=node_color,
        )
        plt.savefig(f"figures/{self.name}/{step}.png")
        # plt.waitforbuttonpress(0.1)

    def draw_time_series(self):
        plt.clf()
        plt.figure(self.name)
        data = np.array(self.time_series_data)
        mean_data = data.mean(axis=0)
        Q1 = np.quantile(data, 0.25, axis=0)
        Q3 = np.quantile(data, 0.75, axis=0)
        x = list(range(self.steps + 1))
        plt.plot(x, mean_data, label="Behavior A")
        plt.fill_between(x, Q1, Q3, alpha=0.3)
        plt.ylim([0, len(self.G)])
        plt.xlabel("Timestep")
        plt.ylabel("# of individuals")
        plt.legend()
        plt.title(f"Agents adopting behavior A for {self.name}")
        plt.savefig(f"figures/{self.name}/timeseries.png")
        plt.close()

    def stats(self):
        data = np.array(self.time_series_data).mean(axis=0)
        stats = {"name": self.name}
        # Time to no changes
        min_sus = data.min()
        stats["time_to_no_change"] = np.where(data == min_sus)[0][0]
        # Percentage adopting
        stats["percentage_adopting"] = data[-1] / len(self.G)
        # Clustering coeffiecient
        stats["clustering_coefficient"] = nx.transitivity(self.G)
        # Density
        stats["density"] = nx.density(self.G)
        # Average path length
        if not nx.is_connected(self.G):
            stats["avg_path_len"] = float("inf")
        else:
            stats["avg_path_len"] = nx.average_shortest_path_length(self.G)

        print(tabulate(stats.values(), headers = stats.keys()))
        return stats

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
