import pygame
from states.modes.online.online_states.waiting_screens import WaitScreen
from states.modes.online.online_states.lobby import Lobby
from states.state import State
from states.modes.online.network import Network
from Constants import *


class Online(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.create_states()

    def update(self):
        if not self.network.connected:
            self.wait_screen.update(self)
        else:
            self.lobby_screen.update(self)

    def render(self):
        if not self.network.connected:
            self.wait_screen.render("ws2")
        else:
            self.lobby_screen.render()

    def create_states(self):
        self.wait_screen = WaitScreen(self.game)
        self.lobby_screen = Lobby(self.game)

    def enter_state(self):
        self.game.screen.blit(pygame.transform.scale(self.game.game_canvas, (WIN_W, WIN_H)), (0, 0))
        self.wait_screen.render("ws1")
        pygame.display.flip()
        pygame.time.delay(600)
        self.network = Network()

    def exit_state(self):
        if self.network.connected:
            self.network.disconnect()
