from maze.simple_maze import SimpleMaze
from agent.A2C import A2CAgent

env = SimpleMaze(render=True)
N_ACTIONS = env.get_action_space()[1][0]
N_STATES = env.get_state_space()[1][0]
LR = 5e-4
MAX_EPISODES = 200
MAX_STEPS = 200

G_list = []
max_G = - MAX_STEPS
agent = A2CAgent(n_states=N_STATES, n_actions=N_ACTIONS, lr=LR)
for i_episode in range(MAX_EPISODES):
    s = env.reset()
    G = 0
    for step in range(1, MAX_STEPS+1):
        action = agent.select_action(s)
        s_, reward, done = env.step(action)
        experience = (s, action, reward, s_, not done)

        agent.learn(experience)
        G += reward
        if done or step == MAX_STEPS:
            if max_G < G:
                agent.save_model()
                max_G = G
            print('{0} done, using {1} steps'.format(i_episode, step))
            G_list.append(G)
            break
