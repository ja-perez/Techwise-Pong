from states.state import State
from Constants import *


class Pause(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)

    def update(self):
        pass

    def render(self):
        pass
