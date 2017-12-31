import gridenv


class SimpleMaze(gridenv.GridEnv):

    def __init__(self):
        super(SimpleMaze, self).__init__()
        

    def _build_env(self):
        pass

    def set_action_space(self, action_space):
        pass
    def reset(self):
        pass

    def step(self, action):
        pass

    def render(self):
        pass


if __name__ == '__main__':
    env = SimpleMaze()
