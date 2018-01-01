import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from .agent import Agent


class A2CNetwork(nn.Module):
    """
    Two-head architecture actor-critic neural network
    """
    def __init__(self, n_states, n_actions):
        super(A2CNetwork, self).__init__()
        self.layer1 = nn.Linear(n_states, 20)
        self.layer2 = nn.Linear(20, 20)
        self.value_head = nn.Linear(20, 1)
        self.policy_head = nn.Linear(20, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu((self.layer2(x)))
        return F.softmax(self.policy_head(x)), self.value_head(x)

    def forward_value(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.value_head(x)

    def forward_policy(self, x):
        x = F.relu((self.layer1(x)))
        x = F.relu((self.layer2(x)))
        return F.softmax(self.policy_head(x))


class A2CAgent(Agent):
    def __init__(self, n_states, n_actions, lr=2e-3, gamma=0.99):
        self.network = A2CNetwork(n_states, n_actions)
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=lr)
        self.gamma = gamma

    def select_action(self, obs):
        obs = torch.FloatTensor(obs).unsqueeze(0)
        obs_var = Variable(obs)
        policy, value = self.network(obs_var)
        action = int(policy.multinomial())
        return action

    def learn(self, experience):
        s, a, r, s_, alive = experience
        s = Variable(torch.FloatTensor(s).unsqueeze(0))
        a = Variable(torch.LongTensor([a]).unsqueeze(0))
        r = Variable(torch.FloatTensor([r]).unsqueeze(0))
        s_ = Variable(torch.FloatTensor(s_).unsqueeze(0))
        alive = Variable(torch.FloatTensor([alive]).unsqueeze(0))

        self.optimizer.zero_grad()
        bellman_target = r + 0.99 * alive * self.network.forward_value(s_)
        estimated_value = self.network.forward_value(s)
        bellman_error = bellman_target - estimated_value
        critic_loss = bellman_error * bellman_error
        critic_loss.backward()
        self.optimizer.step()

        self.optimizer.zero_grad()
        bellman_target = r + 0.99 * alive * self.network.forward_value(s_)
        estimated_value = self.network.forward_value(s)
        bellman_error = bellman_target - estimated_value
        actor_loss = - torch.log(self.network.forward_policy(s).gather(1, a)) * bellman_error
        actor_loss.backward()
        self.optimizer.step()

    def save_model(self, model='./models/a2c_grid.pkl'):
        torch.save(self.network.state_dict(), model)

    def load_model(self, model='./models/a2c_grid.pkl'):
        self.network.load_state_dict(torch.load(model))
