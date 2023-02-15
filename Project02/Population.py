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

        for node_id in early_adopters:
            # Change agent state
            self.population[node_id].state = State.A

        self.counts = self.count_all()

    def count_all(self):
        counts = {}
        for state in State:
            counts[state] = 0
        for agent in self.population:
            counts[agent.state] += 1
        return counts

    def step_all(self):
        for agent in self.population:
            agent.step()
        self.counts = self.count_all()
