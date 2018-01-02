from agent.DeepQ import DeepQAgent
from maze.simple_maze import SimpleMaze


env = SimpleMaze((10, 10), render=True)
N_STATES = env.get_state_space()[1][0]
N_ACTIONS = env.get_action_space()[1][0]
MAX_STEPS = 100000
LEARN_STEPS = 2000
MEM_SIZE = 5000
MAX_EPISODE_STEPS = 200
LR = 2e-3


agent = DeepQAgent(n_actions=N_ACTIONS, n_states=N_STATES,
                   decay_step=LEARN_STEPS, memory_size=MEM_SIZE, lr=LR)
s = env.reset()
best_episodic_rewards = - MAX_EPISODE_STEPS
episode_rewards = 0
episode_counter = 0
for step in range(1, MAX_STEPS+1):
    episode_counter += 1

    action = agent.select_action(s)
    s_, reward, done = env.step(action)
    episode_rewards += reward

    experience = (s, action, reward, s_, not done)
    agent.memorize(experience)
    # transition
    s = s_

    if step > LEARN_STEPS:
        agent.learn()
        agent.episilon_decay()
        agent.update_target_network()

    if done or episode_counter > MAX_EPISODE_STEPS:
        print('Episodic reward:', episode_rewards)

        if episode_rewards > best_episodic_rewards:
            best_episodic_rewards = episode_rewards
            agent.save_model()

        s = env.reset()
        episode_rewards = 0
        episode_counter = 0



print('Training Finished!')

