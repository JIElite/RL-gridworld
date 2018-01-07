import random

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from .agent import Agent
from .memory import DeepQReplayBuffer
from .utils import soft_update_network


class Network(nn.Module):
    def __init__(self, n_states, n_actions):
        super(Network, self).__init__()
        self.layer1 = nn.Linear(n_states, 20)
        self.layer2 = nn.Linear(20, 20)
        self.out = nn.Linear(20, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.out(x)


class DeepQAgent(Agent):
    def __init__(self, n_states, n_actions, lr=2e-3, gamma=0.99, memory_size=10000, epsilon=1.0, min_epsilon=0.1, decay_step=10000):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = (epsilon - min_epsilon) / decay_step
        self.n_actions = n_actions

        self.memory = DeepQReplayBuffer(capacity=memory_size)
        self.evaluate_net = Network(n_states, n_actions)
        self.target_net = Network(n_states, n_actions)
        self.target_net.load_state_dict(self.evaluate_net.state_dict())

        self.optimizer = torch.optim.Adam(self.evaluate_net.parameters(), lr=self.lr)

    def select_action(self, obs):
        if random.uniform(0, 1) > self.epsilon:
            # use greedy policy
            obs = torch.FloatTensor(obs).unsqueeze(0)
            obs_var = Variable(obs)
            action_values = self.evaluate_net(obs_var)
            action = int(action_values.max(1)[1])
        else:
            action = random.randint(0, self.n_actions-1)
        return action

    def learn(self):
        sampled_batch_experience = self.memory.sample()
        batch_s = Variable(torch.FloatTensor(sampled_batch_experience.s))
        batch_a = Variable(torch.LongTensor(sampled_batch_experience.a).unsqueeze(1))
        batch_r = Variable(torch.FloatTensor(sampled_batch_experience.r).unsqueeze(1))
        batch_s_ = Variable(torch.FloatTensor(sampled_batch_experience.s_))
        batch_alive = Variable(torch.FloatTensor(sampled_batch_experience.alive).unsqueeze(1))

        self.optimizer.zero_grad()
        bellman_target = batch_r + batch_alive * self.gamma * self.target_net(batch_s_).max(1)[0].unsqueeze(1)
        estimated_action_values = self.evaluate_net(batch_s).gather(1, batch_a)
        loss = F.smooth_l1_loss(estimated_action_values, bellman_target.detach())
        loss.backward()
        self.optimizer.step()

    def memorize(self, experience):
        self.memory.memorize(experience)

    def episilon_decay(self):
        next_epsilon = self.epsilon - self.decay_rate
        if next_epsilon < self.min_epsilon:
            self.epsilon = self.min_epsilon
        else:
            self.epsilon = next_epsilon

    def update_target_network(self):
        soft_update_network(self.target_net, self.evaluate_net, 0.005)

    def save_model(self, target='./models/dqn_target.pkl', eval='./models/dqn_eval.pkl'):
        torch.save(self.target_net.state_dict(), target)
        torch.save(self.evaluate_net.state_dict(), eval)

    def load_model(self, target='./models/dqn_target.pkl', eval='./models/dqn_eval.pkl'):
        self.target_net.load_state_dict(torch.load(target))
        self.evaluate_net.load_state_dict(torch.load(eval))

