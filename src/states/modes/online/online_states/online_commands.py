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


move_up = False
move_down = False


def up_command(keycode=0, state_inst=None):
    global move_up
    btn_state = {False: "move stop", True: "move up"}
    if keycode == pygame.K_w:
        move_up = not move_up
        state_inst.data = btn_state[move_up]


def down_command(keycode=0, state_inst=None):
    global move_down
    btn_state = {False: "move stop", True: "move down"}
    if keycode == pygame.K_s:
        move_down = not move_down
    state_inst.data = btn_state[move_down]


def leave_command(keycode=0, state_inst=None):
    if keycode == pygame.K_ESCAPE:
        state_inst.online.online_state = state_inst.online.states["lobby"]
        state_inst.data = "leave"


def ready_up(keycode=0, state_inst=None):
    if keycode == pygame.K_SPACE:
        state_inst.data = "ready"
