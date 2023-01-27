from Population import Population


class Experiment:
    def __init__(self, G):
        self.G = G
        self.P = Population(self.G)
        self.steps = 100

    def run(self):
        for i in range(self.steps):
            self.P.step_all()
            self.draw()

    def draw(self):
        pass
