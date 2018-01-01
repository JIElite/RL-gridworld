import random
from abc import abstractmethod


class Agent:
    def __init__(self):
        pass

    @abstractmethod
    def select_action(self, obs):
        pass


class RandomDiscreteAgent(Agent):
    def __init__(self, n_actions):
        self.n_actions = n_actions

    def select_action(self, obs):
        action = random.randint(0, self.n_actions-1)
        return action