import networkx as nx

from Agent import Agent
from State import State


class Population:
    def __init__(self, G, early_adopters):
        self.population = {}
        for i, node in enumerate(G.nodes):
            agent_id = node.id
            neighbors = [n.id for n in nx.all_neighbors(G, node)]
            self.population[agent_id] = Agent(agent_id, neighbors)
        for agent in self.population.values():
            # Assign neighbors to Agent objects
            neighbors = agent.neighbors
            for j in range(len(neighbors)):
                a = neighbors[j]
                if type(a) is int:
                    neighbors[j] = self.population[neighbors[j]]
                else:
                    # Lattice neighbors
                    neighbors[j] = self.population[10 * a[0] + a[1]]

        self.counts = self.count_all()

    def count_all(self):
        A = 0
        B = 0
        for a in self.population:
            if a.state == State.A:
                A += 1
            elif a.state == State.B:
                B += 1
        return A, B

    def step_all(self):
        for agent in self.population:
            agent.step()
        self.counts = self.count_all()
