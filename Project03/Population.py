import networkx as nx

from Agent import Agent
from State import State


class Population:
    def __init__(self, G, early_adopters):
        self.population = {}
        for node in G.nodes:
            neighbors = [n for n in nx.all_neighbors(G, node)]
            self.population[node] = Agent(node, neighbors)
        for agent in self.population.values():
            # Assign neighbors to Agent objects
            neighbors = agent.neighbors
            for j in range(len(neighbors)):
                a = neighbors[j]
                neighbors[j] = self.population[a]

        for node in early_adopters:
            # Change agent state
            self.population[node].current_state = State.STATE_A
            self.population[node].prev_state = State.STATE_A

        self.counts = self.count_all()

    def count_all(self):
        counts = {}
        for state in State:
            counts[state] = 0
        for agent in self.population.values():
            counts[agent.current_state] += 1
        return counts

    def step_all(self):
        for agent in self.population.values():
            agent.step()
        self.counts = self.count_all()
