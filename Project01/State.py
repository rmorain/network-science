from enum import Enum

class State(Enum):
    SUSCEPTIBLE = 'S'
    EXPOSED = 'E'
    INFECTED = 'I'
    RECOVERED = 'R'   
