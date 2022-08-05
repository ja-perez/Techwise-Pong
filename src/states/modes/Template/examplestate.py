from states.state import State
from Constants import *


class Example(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.register_commands()
        self.create_entities()

    def enter_state(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def register_commands(self):
        pass

    def create_entities(self):
        pass

    def set_start_positions(self):
        pass

    def exit_state(self):
        pass
