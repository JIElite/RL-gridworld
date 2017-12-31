import tkinter as tk
from abc import abstractmethod


class Environment:
    def __init__(self, render=False):
        self.__init_render(render)

    @abstractmethod
    def __compute_reward(self, state, action):
        pass

    @abstractmethod
    def __is_terminal(self):
        pass

    def __init_render(self, render=False):
        if render:
            self.renderer = tk.Tk()
        else:
            self.renderer = None

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def get_action_space(self):
        pass

    @abstractmethod
    def get_state_space(self):
        pass

    def render(self):
        if not self.renderer:
            raise ValueError
        else:
            self.renderer.update()


class GridWorld(Environment):

    def __init__(self):
        super(GridWorld, self).__init__()

    @abstractmethod
    def __init_start_pos(self, start_pos):
        pass

    @abstractmethod
    def __init_goal_pos(self, goal_pos_list):
        pass