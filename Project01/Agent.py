import numpy as np
import random
import State

class Agent():

    m_e = 1.0
    s_e = 1.0
    m_i = 2.25
    s_i = 0.105
    B = -0.0050367
    p_1c = 0.12

    def __init__(self, id, neighbors, initial_state=State.SUSCEPTIBLE):
        self.id = id
        self.neighbors = neighbors
        self.state = initial_state
        
        self.days_spent_infectious = 0 # How many days the agent has been infectious
        
        self.d_e = np.ceil(np.random.lognormal(mean=self.m_e, sigma=self.s_e)) # How long the agent stays in the exposed stage
        self.countdown_to_infectious = self.d_e
        self.d_i = np.ceil(np.random.lognormal(mean=self.m_i, sigma=self.s_i)) # How long the agent stays in the infectious stage
        self.countdown_to_recovered = self.d_i
    
    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def step(self):
        if self.state == State.SUSCEPTIBLE:
            self.do_susceptible()
        elif self.state == State.EXPOSED:
            self.do_exposed()
        elif self.state == State.INFECTED:
            self.do_infected()
        else:
            self.do_recovered()

    def do_susceptible(self):
        for neighbor in self.neighbors:
            if neighbor.state == State.INFECTED:
                if Agent.calc_success(neighbor.pInfectionTransmission()):
                    self.setState(State.EXPOSED)
                    return
    
    def do_exposed(self):
        self.countdown_to_infectious-=1
        if self.countdown_to_infectious == 0:
            self.setState(State.INFECTED)
    
    def do_infected(self):
        self.countdown_to_recovered-=1
        self.days_spent_infectious+=1
        if self.countdown_to_recovered==0:
            self.setState(State.RECOVERED)
    
    def do_recovered(self):
        pass
    
    def pInfectionTransmission(self):
        a = self.p_1c / (1 - self.p_1c)
        b = a * np.exp(self.B * (self.days_spent_infectious ** 3 - 1))
        return b / (1 + b)  

    @classmethod
    def calc_success(probability):
        return random.random() < probability

