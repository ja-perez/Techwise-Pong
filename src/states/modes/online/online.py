import pygame
from states.modes.online.online_states.waiting_screens import WaitScreen
from states.modes.online.online_states.lobby import Lobby
from states.state import State
from states.modes.online.network import Network
from Constants import *


class Online(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.friend_code = ""
        self.states = {"waitscreen": WaitScreen(self.game, "waitscreen")}
        self.curr_state = self.states["waitscreen"]

    def update(self):
        if not self.network.connected:
            self.curr_state = self.states["waitscreen"]
        else:
            # self.network.send("test")
            self.curr_state = self.states["lobby"]
        self.curr_state.update(self)

    def render(self):
        if not self.network.connected and self.curr_state.get_name() == "waitscreen":
            self.curr_state.render("ws2")
        else:
            self.curr_state.render()

    def enter_state(self):
        self.game.screen.blit(pygame.transform.scale(self.game.game_canvas, (WIN_W, WIN_H)), (0, 0))
        self.curr_state.render("ws1")
        pygame.display.flip()
        pygame.time.delay(600)
        self.network = Network()
        if self.network.connected:
            self.friend_code = self.network.getP().split()[1]
            self.states.update({"lobby": Lobby(self.game, self)})
            self.curr_state = self.states["lobby"]

    def exit_state(self):
        if self.network.connected:
            self.network.disconnect()
        self.curr_state = self.states["waitscreen"]
