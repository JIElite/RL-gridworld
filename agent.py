from .IMemorizable import IMemorizable

class Agent:
    def __init__(self):
        pass

    def select_action(self):
        pass

    def learn(self):
        pass


class MemorizedAgent(Agent, IMemorizable):
    pass