from commands.command import *
from inspect import signature
from states.state import State


class LocalCommand(ICommand):
    def __init__(self, active: ActiveOn, function: Callable, state: State):
        super(LocalCommand, self).__init__(active, function)
        self.state = state

    def execute(self, keycode):
        if len(signature(self.function).parameters) >= 1:
            self.function(keycode, self.state)
        else:
            self.function()

    def undo(self):
        pass


def player_commands(keycode=0, state=0):
    pass
