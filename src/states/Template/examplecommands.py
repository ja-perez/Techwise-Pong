from commands.command import *
from inspect import signature
from commands.command import ICommand

class ExampleCommand(ICommand):
    def __init__(self, active: ActiveOn, function: Callable, state_inst: State):
        super(LocalCommand, self).__init__(active, function)
        self.state_inst = state_inst

    def execute(self, keycode):
        if len(signature(self.function).parameters) >= 1:
            self.function(keycode, self.state_inst)
        else:
            self.function()

    def undo(self):
        pass


def example_command(keycode=0, state_inst=None):
    pass