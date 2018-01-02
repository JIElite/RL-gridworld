from abc import abstractmethod


class Grid:
    def __init__(self, x, y):
        self.set_position(x, y)

    def get_rectangle_pos(self, unit_size):
        return (self.x*unit_size, self.y*unit_size, (self.x+1)*unit_size, (self.y+1)*unit_size)

    def is_terminal(self):
        return False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    @abstractmethod
    def effect(self, agent_state):
        pass

    @abstractmethod
    def render(self, canvas, unit_size):
        pass


class EmptyGrid(Grid):
    def effect(self, agent_state):
        return agent_state

    def render(self, canvas, unit_size):
        pass


class TerminalGrid(Grid):
    def effect(self, agent_state):
        return agent_state

    def render(self, canvas, unit_size):
        canvas.create_rectangle(
            *self.get_rectangle_pos(unit_size),
            fill='yellow'
        )


    def is_terminal(self):
        return True


class WallGrid(Grid):
    def effect(self, agent_state):
        # 比較 tricky 的地方是 WallGrid 的效果相當於不能讓 agent 踩到這個位置
        # 也就是返回上一步
        agent_previous_pos = agent_state.get_previous_state()
        agent_state.update_state(agent_previous_pos)
        return agent_state

    def render(self, canvas, unit_size):
        canvas.create_rectangle(
            *self.get_rectangle_pos(unit_size),
            fill='black'
        )
