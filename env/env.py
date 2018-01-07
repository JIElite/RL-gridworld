from abc import abstractmethod
import tkinter as tk

from .agent import GridAgent
from .grid import EmptyGrid


class Environment:
    def __init__(self, render=False):
        self.renderable = render
        self.renderer = None
        self.action_space = None
        self.state_space = None
        self.agent = None

    @abstractmethod
    def __compute_reward(self, state, action):
        pass

    @abstractmethod
    def __is_terminal(self):
        pass

    @abstractmethod
    def __init_render(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def get_state(self):
        pass

    def set_action_space(self, action_space):
        self.action_space = action_space

    def get_action_space(self):
        return self.action_space, self.action_space.shape

    def set_state_space(self, state_space):
        self.state_space =  state_space

    def get_state_space(self):
        return self.state_space, self.state_space.shape

    def render(self):
        if not self.renderer:
            raise ValueError
        else:
            self.renderer.update()


class GridWorld(Environment):
    def __init__(self, grid_size=(10, 10), unit_size=40, render=False):
        super(GridWorld, self).__init__(render=render)
        self.maze_grids = []
        self.start_pos = (0, 0)
        self.goal_pos_list = []
        self.grid_size = grid_size
        self.unit_size = unit_size
        self.canvas = None
        self.__init__render()

    @abstractmethod
    def init_start_pos(self):
        pass

    @abstractmethod
    def init_goal_pos(self):
        pass

    @abstractmethod
    def init_grid_world(self):
        pass

    def __init__render(self):
        if self.renderable:
            self.renderer = tk.Tk()
            self.renderer.title(self.__class__.__name__)
            self.renderer.geometry('{0}x{1}'.format(
                self.grid_size[0]*self.unit_size,
                self.grid_size[1]*self.unit_size,
            ))
            self.canvas = tk.Canvas(self.renderer, bg='white',
                                    height=self.grid_size[1]*self.unit_size,
                                    width=self.grid_size[0]*self.unit_size
                                    )
            self.canvas.pack()

    def draw_grid_worlds(self):
        # draw grid line
        for c in range(0, self.grid_size[0] * self.unit_size, self.unit_size):
            x0, y0, x1, y1 = c, 0, c, self.grid_size[1] * self.unit_size
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, self.grid_size[1] * self.unit_size, self.unit_size):
            x0, y0, x1, y1 = 0, r, self.grid_size[0] * self.unit_size, r
            self.canvas.create_line(x0, y0, x1, y1)

         # fill differernt grids
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                self.maze_grids[y][x].render(self.canvas, self.unit_size)

    def init_empty_grids(self):
        for y in range(self.grid_size[1]):
            self.maze_grids.append([])
            for x in range(self.grid_size[0]):
                self.maze_grids[y].append(EmptyGrid(x, y))

    def set_grid_size(self, grid_size):
        self.grid_size = grid_size

    def get_grid_size(self):
        return self.grid_size

    def set_unit_size(self, unit_size):
        self.unit_size = unit_size

    def get_unit_size(self):
        return self.unit_size

    def get_state(self):
        if isinstance(self.agent, GridAgent):
            return self.agent.get_current_state()
        else:
            raise ValueError('Attribute self.agent does not GridAgent.')
