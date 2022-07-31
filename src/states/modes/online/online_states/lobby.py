import pygame, pygwidgets
from states.state import State
from ecs.entities import State_Text
from Constants import *


class Lobby(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.create_objects()

    def update(self, state):
        for event in pygame.event.get():
            if self.find_match_btn.handleEvent(event):
                pass
            elif self.mainmenu_btn.handleEvent(event):
                state.change_state("mainmenu")

    def render(self):
        graphic_component = self.lobby_screen.components["graphics"]
        self.game.screen.blit(graphic_component.surface, graphic_component.rect)
        self.find_match_btn.draw()
        self.mainmenu_btn.draw()

    def create_objects(self):
        # Lobby title
        lobby_title = "Lobby"
        self.lobby_screen = State_Text(lobby_title, TEXT_SIZE, WHITE)
        graphic_component = self.lobby_screen.components["graphics"]
        self.lobby_screen.set_pos(GAME_W - graphic_component.rect.width / 2,
                                  GAME_H - graphic_component.rect.height * 2)

        # Lobby Buttons
        self.find_match_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Find Match')
        btn_rect = self.find_match_btn.getRect().width, self.find_match_btn.getRect().height
        self.find_match_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2)
        self.mainmenu_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Main Menu')
        btn_rect = self.mainmenu_btn.getRect().width, self.mainmenu_btn.getRect().height
        self.mainmenu_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2
                                 + btn_rect[1])
