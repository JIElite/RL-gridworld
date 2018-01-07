from .simple_maze import  SimpleMaze


class Maze2(SimpleMaze):
    def __init__(self, grid_size=(10, 10), unit_size=40, render=False):
        super(Maze2, self).__init__(grid_size, unit_size, render)

    def init_start_pos(self):
        self.start_pos = (0, 0)

    def init_wall_pos(self):
        self.wall_pos_list = [(1, 1), (1, 2), (2, 1), (6, 6), (7, 7), (8, 8), (1, 8)]

    def init_goal_pos(self):
        self.goal_pos_list = [(5, 7), (9, 1)]

