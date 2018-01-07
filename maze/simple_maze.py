import numpy as np

from env import env
from env.grid import GoalGrid, WallGrid
from env.agent import GridAgent


class SimpleMaze(env.GridWorld):
    def __init__(self, grid_size=(10, 10), unit_size=40, render=False):
        super(SimpleMaze, self).__init__(grid_size=grid_size, unit_size=unit_size, render=render)
        self.init_grid_world()
        self.set_action_space(np.array(['up', 'down', 'left', 'right']))
        self.set_state_space(np.array(['x', 'y']))
        self.agent = GridAgent(self.start_pos[0], self.start_pos[1], self.canvas)

    def init_grid_world(self):
        self.init_start_pos()
        self.init_goal_pos()
        self.init_wall_pos()

        self.init_empty_grids()
        self.init_goal_grids()
        self.init_wall_grids()

        if self.renderable:
            self.draw_grid_worlds()

    def init_start_pos(self):
        self.start_pos = (0, 0)

    def init_goal_pos(self):
        self.goal_pos_list = [(5, 7), (9, 1)]

    def init_goal_grids(self):
        for goal_pos in self.goal_pos_list:
            x, y = goal_pos[0], goal_pos[1]
            self.maze_grids[y][x] = GoalGrid(x, y)

    def init_wall_pos(self):
        self.wall_pos_list = [(1, 1), (1, 2), (2, 1)]

    def init_wall_grids(self):
        for wall_pos in self.wall_pos_list:
            x, y = wall_pos[0], wall_pos[1]
            self.maze_grids[y][x] = WallGrid(x, y)

    def reset(self):
        # initialize agent state, and return the observation
        self.agent.reset()
        return self.get_state()

    def get_action_space(self):
        return self.action_space, self.action_space.shape

    def get_state_space(self):
        return self.state_space, self.state_space.shape

    def step(self, action):

        # TODO
        # 能不能對應到 action space 用 action space 來做處理？
        current_pos = self.agent.get_current_state()
        if action == 0:
            # move up
            next_pos = [current_pos[0], current_pos[1]-1]
        elif action == 1:
            # move down
            next_pos = [current_pos[0], current_pos[1]+1]
        elif action == 2:
            # move left
            next_pos = [current_pos[0]-1, current_pos[1]]
        elif action == 3:
            # move right
            next_pos = [current_pos[0]+1, current_pos[1]]
        else:
            raise ValueError

        max_y = self.grid_size[1] - 1
        min_y = 0
        max_x = self.grid_size[0] - 1
        min_x = 0

        if next_pos[0] > max_x:
            next_pos[0] = max_x
        elif next_pos[0] < min_x:
            next_pos[0] = min_x

        if next_pos[1] > max_y:
            next_pos[1] = max_y
        elif next_pos[1] < min_y:
            next_pos[1] = min_y

        # transition
        # 當 agent 決定出移動的下一步之後，先做移動，再看看那個 grid 是不是有什麼效果？
        self.agent.update_state(next_pos)
        self.maze_grids[next_pos[1]][next_pos[0]].effect(self.agent)

        done = self.__is_terminal()
        reward = self.__compute_reward(self.agent.get_previous_state(), action)
        return self.get_state(), reward, done

    def __is_terminal(self):
        return self.agent.get_current_state() in self.goal_pos_list

    def __compute_reward(self, state, action):
        if self.__is_terminal():
            reward = 20
        else:
            reward = -1
        return reward

    def render(self):
        if not (self.renderer and self.canvas):
            raise ValueError('Renderer does not exist!')
        self.agent.render(self.unit_size)
        self.renderer.update()