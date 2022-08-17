import pygame, pygwidgets
from states.state import State
from ecs.entities import State_Text
from states.modes.online.online_states.r_match import OnlineMatch
from Constants import *


class Lobby(State):
    def __init__(self, online):
        State.__init__(self, online.game)
        self.online = online
        self.create_objects()

    def update(self):
        for event in pygame.event.get():
            if self.join_public_btn.handleEvent(event):
                self.online.states.update({"match": OnlineMatch(self.online)})
                self.online.online_state = self.online.states["match"]
                self.online.online_state.enter_state()
            elif self.join_private_btn.handleEvent(event):
                self.online.states.update({"match": OnlineMatch(self.online, True)})
                self.online.online_state = self.online.states["match"]
                self.online.online_state.enter_state()
            elif self.mainmenu_btn.handleEvent(event):
                self.online.exit_online()

    def render(self):
        graphic_component = self.lobby_screen.components["graphics"]
        self.game.screen.blit(graphic_component.surface, graphic_component.rect)
        self.join_public_btn.draw()
        self.join_private_btn.draw()
        self.mainmenu_btn.draw()

    # Creating the graphical components of this state
    def create_objects(self):
        self.create_texts()
        self.create_buttons()

    def create_texts(self):
        # Lobby title
        lobby_title = "Lobby"
        self.lobby_screen = State_Text(lobby_title, TEXT_SIZE, WHITE)
        graphic_component = self.lobby_screen.components["graphics"]
        self.lobby_screen.set_pos(GAME_W - graphic_component.rect.width / 2,
                                  GAME_H - graphic_component.rect.height * 2)

    def create_buttons(self):
        # Lobby Buttons
        # Find Random Match
        self.join_public_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Find Match')
        btn_rect = self.join_public_btn.getRect().width, self.join_public_btn.getRect().height
        self.join_public_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2)
        # Play with friend
        self.join_private_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Play with Friend')
        btn_rect = self.join_private_btn.getRect().width, self.join_private_btn.getRect().height
        self.join_private_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2
                                      + btn_rect[1])
        # Return to main menu
        self.mainmenu_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Main Menu')
        btn_rect = self.mainmenu_btn.getRect().width, self.mainmenu_btn.getRect().height
        self.mainmenu_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2
                                 + btn_rect[1] * 2)

    def reset(self):
        pass