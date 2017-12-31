import tkinter
from env import Environment


class GridEnv(Environment, tkinter.Tk):

    def __init__(self):
        super().__init__()

    def _build_env(self):
        pass
