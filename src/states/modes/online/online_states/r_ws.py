import pygame, pygwidgets
from states.state import State
from ecs.entities import State_Text
from Constants import *
from states.modes.online.network import Network

class WaitScreen(State):
    def __init__(self, online, name):
        State.__init__(self, online.game, name)
        self.online = online
        self.create_scenes()
        self.conn_attempt = False

    def update(self):
        if not self.conn_attempt:
            self.online.network = Network()
            pygame.time.delay(300)
            if self.online.network.connected:
                self.online.client_id = self.online.network.get_id()
                self.online.online_state = self.online.states["lobby"]
            else:
                self.conn_attempt = True
        else:
            for event in pygame.event.get():
                if self.ws2_button1.handleEvent(event):
                    self.conn_attempt = False
                elif self.ws2_button2.handleEvent(event):
                    self.online.exit_online()

    def render(self):
        if not self.conn_attempt:
            graphic_component = self.wait_screen1.components["graphics"]
            self.game.screen.blit(graphic_component.surface, graphic_component.rect)
        else:
            graphic_component = self.wait_screen2.components["graphics"]
            self.game.screen.blit(graphic_component.surface, graphic_component.rect)
            self.ws2_button1.draw()
            self.ws2_button2.draw()

    def create_scenes(self):
        # waiting screen 1
        ws1_text = "Waiting for response from server"
        self.wait_screen1 = State_Text(ws1_text, TEXT_SIZE, WHITE)
        graphic_component = self.wait_screen1.components["graphics"]
        self.wait_screen1.set_pos(GAME_W - graphic_component.rect.width / 2,
                                  GAME_H - graphic_component.rect.height / 2)
        # WIP: Create an animated loading icon

        # waiting screen 2
        ws2_text = "No response from server, try again?"
        self.wait_screen2 = State_Text(ws2_text, TEXT_SIZE, WHITE)
        graphic_component = self.wait_screen2.components["graphics"]
        self.wait_screen2.set_pos(GAME_W - graphic_component.rect.width / 2,
                                  GAME_H - graphic_component.rect.height * 2)
        # waiting screen 2 buttons
        self.ws2_button1 = pygwidgets.TextButton(self.game.screen, (0, 0), 'Yes')
        btn_rect = self.ws2_button1.getRect().width, self.ws2_button1.getRect().height
        self.ws2_button1.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2)

        self.ws2_button2 = pygwidgets.TextButton(self.game.screen, (0, 0), 'No')
        btn_rect = self.ws2_button2.getRect().width, self.ws2_button2.getRect().height
        self.ws2_button2.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2
                                + btn_rect[1])

    def reset(self):
        self.conn_attempt = False