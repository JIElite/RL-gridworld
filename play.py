from agent.A2C import A2CAgent
from maze.simple_maze import SimpleMaze
import time

env = SimpleMaze((10, 10), render=True)
N_STATES = env.get_state_space()[1][0]
N_ACTIONS = env.get_action_space()[1][0]
MAX_EPISODES = 20000
MAX_STEPS = 200

agent = A2CAgent(n_actions=N_ACTIONS, n_states=N_STATES)
agent.load_model()

for i_episode in range(MAX_EPISODES):
    s = env.reset()
    for step in range(1, MAX_STEPS+1):
        env.render()
        time.sleep(0.05)
        action = agent.select_action(s)
        s_, reward, done = env.step(action)

        if done or step == MAX_STEPS:
            env.render()
            print('Episode:{0} done. step:{1}'.format(i_episode, step))
            break
