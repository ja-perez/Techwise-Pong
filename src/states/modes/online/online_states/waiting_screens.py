import pygame, pygwidgets
from states.state import State
from ecs.entities import State_Text
from Constants import *


class WaitScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.create_scenes()

    def update(self, state):
        for event in pygame.event.get():
            if self.ws2_button1.handleEvent(event):
                state.enter_state()
            elif self.ws2_button2.handleEvent(event):
                state.change_state("mainmenu")

    def render(self, scene):
        if scene == "ws1":
            graphic_component = self.wait_screen1.components["graphics"]
            self.game.screen.blit(graphic_component.surface, graphic_component.rect)
        elif scene == "ws2":
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
