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


move_up = 0
move_down = 0


def up_command(keycode=0, state_int=None):
    global move_up
    btn_state = {0: "move stop", 1: "move up"}
    if keycode == pygame.K_w:
        move_up = int(not move_up)
        state_int.data = btn_state[move_up]


def down_command(keycode=0, state_int=None):
    global move_down
    btn_state = {0: "move stop", 1: "move down"}
    if keycode == pygame.K_s:
        move_down = int(not move_down)
    state_int.data = btn_state[move_down]
