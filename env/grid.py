from abc import abstractmethod


class Grid:
    @abstractmethod
    def effect(self, agent_state):
        pass

    @abstractmethod
    def render(self):
        pass

    def is_terminal(self):
        return False


class EmptyGrid(Grid):
    def render(self):
        pass

    def effect(self, agent_state):
        # None effect
        pass


class TerminalGrid(Grid):
    def effect(self, agent_state):
        # None effect
        pass

    def render(self):
        pass

    def is_terminal(self):
        return True


class WallGrid(Grid):
    def effect(self, agent_state):
        # Like get back to previous step
        previous_pos = agent_state[0]
        agent_state[1] = previous_pos

    def render(self):
        pass

