from env import env
import numpy as np
import random


class SimpleMaze(env.GridWorld):
    def __init__(self, grid_size=(10, 10), unit_size=40, render=False):
        self.action_space = np.array(['up', 'down', 'left', 'right'])
        self.observation_space = np.array(['x', 'y'])
        self.grid_size = grid_size
        self.unit_size = unit_size

        self.start_pos = [0, 0]
        self.goal_pos_list = [(5, 7), (9, 1)]
        self.barrier_pos_list = [(6, 6), (2, 3), (5, 5)]
        self.reset()

    def __build_maze(self, start_pos, goal_pos_list, barrier_pos_list):
        self.__init_start_pos(start_pos)
        self.__init_goal_state(goal_pos_list)
        self.__init_barrier(barrier_pos_list)

        self.maze = np.zeros(self.grid_size)
        for goal_pos in self.goal_pos_list:
            self.maze[goal_pos] = 3
        for barrier_pos in self.barrier_pos_list:
            self.maze[barrier_pos] = 2

    def __init_start_pos(self, start_pos=(0, 0)):
        self.agent_pos = start_pos
        self.agent_last_pos = start_pos

    def __init_barrier(self, barrier_list):
        self.barrier_pos_list = barrier_list

    def __init_goal_state(self, goal_pos_list):
        self.goal_pos_list = goal_pos_list

    def reset(self):
        self.__build_maze(self.start_pos, self.goal_pos_list, self.barrier_pos_list)
        return self.agent_pos

    def get_action_space(self):
        return self.action_space, self.action_space.shape

    def get_state_space(self):
        return self.observation_space, self.observation_space.shape

    def step(self, action):
        current_pos = self.agent_pos
        if action == 0:
            # move up
            next_pos = [current_pos[0] - 1, current_pos[1]]
        elif action == 1:
            # move down
            next_pos = [current_pos[0] + 1, current_pos[1]]
        elif action == 2:
            # move left
            next_pos = [current_pos[0], current_pos[1] - 1]
        elif action == 3:
            # move right
            next_pos = [current_pos[0], current_pos[1] + 1]
        else:
            raise ValueError

        if next_pos[0] > 9:
            next_pos[0] = 9
        elif next_pos[0] < 0:
            next_pos[0] = 0

        if next_pos[1] > 9:
            next_pos[1] = 9
        elif next_pos[1] < 0:
            next_pos[1] = 0

        next_pos = tuple(next_pos)
        # transition
        if self.maze[next_pos] == 0:
            current_pos = next_pos
        elif self.maze[next_pos] == 3:
            current_pos = next_pos
        else:
            # remain position
            pass

        self.agent_last_pos = self.agent_pos
        self.agent_pos = current_pos

        done = self.__is_terminal()
        reward = self.__compute_reward(self.agent_last_pos, action)
        return self.agent_pos, reward, done

    def __is_terminal(self):
        return self.agent_pos in self.goal_pos_list

    def __compute_reward(self, state, action):
        if self.__is_terminal():
            reward = 0
        else:
            reward = -1

        return reward

if __name__ == '__main__':
    env = SimpleMaze()
    s = env.reset()

    for step in range(10000):
        action = random.randint(0, 3)
        s_, reward, done = env.step(action)
        print(s, action, reward, s_)
        s = s_
        if done:
            print("done", step)
            break
