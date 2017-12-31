from agent.IMemorizable import IMemorizable
import random
from abc import abstractmethod


class Agent:
    def __init__(self):
        pass

    @abstractmethod
    def select_action(self, obs):
        pass

    @abstractmethod
    def learn(self):
        pass


class RandomDiscreteAgent(Agent):

    def __init__(self, n_actions):
        self.set_action_space(n_actions)

    def set_action_space(self, n_actions):
        self.n_actions = n_actions

    def select_action(self, obs):
        action = random.randint(0, self.n_actions-1)
        return action