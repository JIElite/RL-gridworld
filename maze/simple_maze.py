import tkinter as tk

import numpy as np

from env import env
from env.grid import EmptyGrid, TerminalGrid, WallGrid
from env.agent import GridAgent


class SimpleMaze(env.GridWorld):
    def __init__(self, grid_size=(10, 10), unit_size=40, render=False):
        # super(SimpleMaze, self).__init__(render)
        self.action_space = np.array(['up', 'down', 'left', 'right'])
        self.observation_space = np.array(['x', 'y'])
        self.grid_size = grid_size
        self.unit_size = unit_size

        # initialize maze
        self.goal_pos_list = [(5, 7), (9, 1)]
        self.barrier_pos_list = [(1, 1), (1, 2), (2, 1)]
        self.__build_maze(self.goal_pos_list, self.barrier_pos_list)

        # initialize agent's state
        self.start_pos = (0, 0)
        self.reset()
        self.__init_render(render)

    def __build_maze(self, goal_pos_list, barrier_pos_list):
        self.__init_goal_state(goal_pos_list)
        self.__init_barrier(barrier_pos_list)
        self.__init_grids()
        for goal_pos in self.goal_pos_list:
            x, y = goal_pos[0], goal_pos[1]
            self.maze_grids[y][x] = TerminalGrid(x, y)

        for barrier_pos in self.barrier_pos_list:
            x, y = barrier_pos[0], barrier_pos[1]
            self.maze_grids[y][x] = WallGrid(x, y)

    def __init_barrier(self, barrier_list):
        self.barrier_pos_list = barrier_list

    def __init_goal_state(self, goal_pos_list):
        self.goal_pos_list = goal_pos_list

    def __init_grids(self):
        self.maze_grids = []
        for y in range(self.grid_size[1]):
            self.maze_grids.append([])
            for x in range(self.grid_size[0]):
                self.maze_grids[y].append(EmptyGrid(x, y))

    def reset(self):
        # initialize agent state, and return the observation
        self.agent = GridAgent(self.start_pos[0], self.start_pos[1])
        return self.agent.get_current_state()

    def get_action_space(self):
        return self.action_space, self.action_space.shape

    def get_state_space(self):
        return self.observation_space, self.observation_space.shape

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
        return self.agent.get_current_state(), reward, done

    def __is_terminal(self):
        return self.agent.get_current_state() in self.goal_pos_list

    def __compute_reward(self, state, action):
        if self.__is_terminal():
            reward = 0
        else:
            reward = -1

        return reward

    def __init_render(self, render):
        if render:
            self.renderer = tk.Tk()
            self.renderer.title('SimpleMaze')
            self.renderer.geometry('{0}x{1}'.format(
                self.grid_size[1]*self.unit_size,
                self.grid_size[1]*self.unit_size,
            ))
            self.canvas = tk.Canvas(self.renderer, bg='white',
                                    height=self.grid_size[1]*self.unit_size,
                                    width=self.grid_size[1]*self.unit_size
                                    )
            self.canvas.pack()

            for c in range(0, self.grid_size[0] * self.unit_size, self.unit_size):
                x0, y0, x1, y1 = c, 0, c, self.grid_size[0] * self.unit_size
                self.canvas.create_line(x0, y0, x1, y1)
            for r in range(0, self.grid_size[1] * self.unit_size, self.unit_size):
                x0, y0, x1, y1 = 0, r, self.grid_size[1] * self.unit_size, r
                self.canvas.create_line(x0, y0, x1, y1)

            for y in range(self.grid_size[1]):
                for x in range(self.grid_size[0]):
                    self.maze_grids[y][x].render(self.canvas, self.unit_size)

        else:
            self.renderer = None

    def render(self):
        if not (self.renderer and self.canvas):
            raise ValueError('Renderer does not exist!')

        self.agent.render(self.canvas, self.unit_size)
        self.renderer.update()

