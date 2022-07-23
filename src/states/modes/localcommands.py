from commands.command import *
from inspect import signature
from states.state import State
import pygame

class LocalCommand(ICommand):
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


def up_command(keycode=0, state_int=0):
    if keycode == pygame.K_w:
        state_int.p1_up = not state_int.p1_up
    elif keycode == pygame.K_UP:
        state_int.p2_up = not state_int.p2_up
    print(state_int.p1_up)

def down_command(keycode=0, state_int=0):
    if keycode == pygame.K_s:
        state_int.p1_down = not state_int.p1_down
    elif keycode == pygame.K_DOWN:
        state_int.p2_down = not state_int.p2_down

def set_start(keycode=0, state_inst=0):
    state_inst.start = not state_inst.start
