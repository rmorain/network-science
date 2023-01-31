import networkx as nx
import numpy as np

from Agent import Agent
from State import State


class Population:
    def __init__(self, G):
        N = len(G.nodes)
        self.population = []
        for i, node in enumerate(G.nodes):
            neighbors = [n for n in nx.all_neighbors(G, node)]
            self.population.append(Agent(i, neighbors))
        for i in range(N):
            # Assign neighbors to Agent objects
            A = self.population[i]
            neighbors = A.neighbors
            for j in range(len(neighbors)):
                a = neighbors[j]
                if type(a) is int:
                    neighbors[j] = self.population[neighbors[j] - 1]
                else:
                    # Lattice neighbors
                    neighbors[j] = self.population[10 * a[0] + a[1]]

        # Set 5% of the population to exposed and 5% to infectious
        exposed_infectious = np.random.choice(
            self.population, size=int(N * 0.1), replace=False
        )
        for i in range(len(exposed_infectious) // 2):
            exposed_infectious[i].state = State.EXPOSED
        for i in range(len(exposed_infectious) // 2, len(exposed_infectious)):
            exposed_infectious[i].state = State.INFECTED
        self.counts = self.count_all()

    def count_all(self):
        susceptible = 0
        exposed = 0
        infectious = 0
        recovered = 0
        for a in self.population:
            if a.state == State.SUSCEPTIBLE:
                susceptible += 1
            elif a.state == State.EXPOSED:
                exposed += 1
            elif a.state == State.INFECTED:
                infectious += 1
            elif a.state == State.RECOVERED:
                recovered += 1
        return susceptible, exposed, infectious, recovered

    def step_all(self):
        for agent in self.population:
            agent.step()
        self.counts = self.count_all()
