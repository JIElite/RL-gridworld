class Environment:
    def __init__(self):
        self._build_env()
        self.reset()

    def _build_env(self):
        pass

    def set_action_space(self, action_space):
        self.action_space = action_space

    def reset(self):
        pass

    def step(self, action):
        pass

    def render(self):
        pass
