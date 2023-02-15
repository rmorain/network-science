import unittest

from Agent import Agent


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.A = Agent(0, [Agent(1, [])])

    def test_step(self):
        self.A.step()


if __name__ == "__main__":
    unittest.main()
