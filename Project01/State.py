from enum import Enum

class State(Enum):
    SUSCEPTIBLE = 'blue'
    EXPOSED = 'yellow'
    INFECTED = 'red'
    RECOVERED = 'green'   
