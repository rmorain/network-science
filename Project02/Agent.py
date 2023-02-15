import random

import numpy as np

from State import State


class Agent:

    payoff_a=3
    payoff_b=2

    def __init__(self, id, neighbors, initial_state=State.STATE_B):
        self.id = id
        self.neighbors = neighbors
        self.state = initial_state

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def step(self):
        if self.state == State.STATE_B:
            ua,ub=0,0
            for neighbor in self.neighbors:
                if neighbor.state == State.STATE_B:
                    ub+=self.payoff_b
                else:
                    ua+=self.payoff_a
            if ua>ub:
                self.setState(State.STATE_A)

    def calc_success(self, probability):
        return random.random() < probability
