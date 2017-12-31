from maze.simple_maze import SimpleMaze
from agent.agent import  RandomDiscreteAgent


env = SimpleMaze()
MAX_STEPS = 1000
N_ACTIONS = env.get_action_space()[1][0]



agent = RandomDiscreteAgent(n_actions=N_ACTIONS)

s = env.reset()
for step in range(MAX_STEPS):
    action = agent.select_action(s)
    s_, reward, done = env.step(action)
    s = s_

    if done:
        print("done", step)
        break

