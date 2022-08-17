import pygame
from states.state import State
from states.modes.online.online_states.r_lobby import Lobby
from states.modes.online.online_states.r_ws import WaitScreen


class Online(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.states = {"waitscreen": WaitScreen(self, "waitscreen"),
                       "lobby": Lobby(self),
                       "match": None}
        self.online_state = self.states["waitscreen"]
        self.network = None
        self.client_id = 0

    def update(self):
        self.online_state.update()

    def render(self):
        self.online_state.render()

    def enter_state(self):
        self.online_state = self.states["waitscreen"]
        # Reset screen to show waiting screen 1
        self.game.reset_screen()
        self.online_state.render()

    def exit_online(self):
        # disconnect from server if connected
        if self.network.connected:
            self.network.disconnect()
        # Reset the current state
        self.online_state.reset()
        # Change Game state to the mainmenu
        self.change_state("mainmenu")
