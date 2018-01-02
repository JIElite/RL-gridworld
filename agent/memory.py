import random
from collections import namedtuple, deque
from abc import abstractmethod


Transition = namedtuple('Transition', ['s', 'a', 'r', 's_', 'alive'])


class Memory:
    @abstractmethod
    def memorize(self, experience):
        pass

    @abstractmethod
    def sample(self, sample_size=32):
        pass


class DeepQReplayBuffer(Memory):
    def __init__(self, capacity=10000):
        self.capacity = capacity
        self.memory = deque(maxlen=self.capacity)

    def memorize(self, experience):
        self.memory.append(Transition(*experience))

    def sample(self, sample_size=32):
        current_length = len(self.memory)
        if current_length < sample_size:
            sample_size = current_length

        sampled_experience = random.sample(self.memory, sample_size)
        return Transition(*zip(*sampled_experience))


