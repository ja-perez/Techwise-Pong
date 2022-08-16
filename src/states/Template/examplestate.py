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
        command_queue = self.ih.handle_input()
        for command, args in command_queue:
            command.execute(args[0])

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
