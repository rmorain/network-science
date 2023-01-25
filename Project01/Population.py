import numpy as np
import Agent
import State

class Population():
    def __init__(self, G, m_e=1.0, s_e=1.0, m_i=2.25, s_i=0.105):
        N = len(G.nodes)
        self.population = []
        for i in range(N):
            neighbors = G[i]
            self.population.append(Agent(m_e, s_e, m_i, s_i, neighbors))
        # Set 5% of the population to exposed and 5% to infectious
        exposed_infectious = np.random.choice(self.population, size=int(N * 0.1), replace=False)
        for i in range(len(exposed_infectious) // 2):
            exposed_infectious[i].state = State.EXPOSED
        for i in range(len(exposed_infectious) // 2, len(exposed_infectious)):
            exposed_infectious[i].state = State.INFECTED
            
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
        for a in self.all:
            a.step()