from abc import abstractmethod


class Environment:
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
    @abstractmethod
    def __init_start_pos(self, start_pos):
        pass

    @abstractmethod
    def __init_goal_pos(self, goal_pos_list):
        pass

    @abstractmethod
    def __init_grids(self):
        pass