import pygame
from commands.command import *
from inspect import signature
from states.state import State

class MatchCommand(ICommand):
    def __init__(self, active: ActiveOn, function: Callable, state_inst: State):
        super(MatchCommand, self).__init__(active, function)
        self.state_inst = state_inst

    def execute(self, keycode):
        if len(signature(self.function).parameters) >= 1:
            self.function(keycode, self.state_inst)
        else:
            self.function()

    def undo(self):
        pass


def up_command(keycode=0, state_int=None):
    if keycode == pygame.K_w:
        state_int.server_response = state_int.network.send("move up")


def down_command(keycode=0, state_int=None):
    if keycode == pygame.K_s:
        state_int.server_response = state_int.network.send("move down")
