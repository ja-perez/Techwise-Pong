import pygame, pygwidgets
from states.state import State
from ecs.entities import State_Text
from states.modes.online.online_states.friend_screen import Friend_Screen
from states.modes.online.online_states.online_match import Online_Match
from Constants import *


class Lobby(State):
    def __init__(self, game, online):
        State.__init__(self, game)
        self.create_objects()
        self.online_inst = online
        self.states = {"friendscreen": Friend_Screen(game, online),
                       "publicmatch": Online_Match(game, online),
                       "privatematch": Online_Match(game, online, True),
                       "self": self}
        self.curr_state = self.states["self"]

    def update(self, state):
        if self.curr_state != self:
            self.curr_state.update(self)
        else:
            for event in pygame.event.get():
                if self.find_match_btn.handleEvent(event):
                    self.change_online_state("publicmatch")
                elif self.play_w_friend_btn.handleEvent(event):
                    self.curr_state = self.states["friendscreen"]
                elif self.mainmenu_btn.handleEvent(event):
                    state.change_state("mainmenu")

    def render(self):
        if self.curr_state != self:
            self.curr_state.render()
        else:
            graphic_component = self.lobby_screen.components["graphics"]
            self.game.screen.blit(graphic_component.surface, graphic_component.rect)
            self.find_match_btn.draw()
            self.play_w_friend_btn.draw()
            self.mainmenu_btn.draw()

    def create_objects(self):
        # Lobby title
        lobby_title = "Lobby"
        self.lobby_screen = State_Text(lobby_title, TEXT_SIZE, WHITE)
        graphic_component = self.lobby_screen.components["graphics"]
        self.lobby_screen.set_pos(GAME_W - graphic_component.rect.width / 2,
                                  GAME_H - graphic_component.rect.height * 2)

        # Lobby Buttons
        # Find Random Match
        self.find_match_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Find Match')
        btn_rect = self.find_match_btn.getRect().width, self.find_match_btn.getRect().height
        self.find_match_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2)
        # Play with friend
        self.play_w_friend_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Play with Friend')
        btn_rect = self.play_w_friend_btn.getRect().width, self.play_w_friend_btn.getRect().height
        self.play_w_friend_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2
                                  + btn_rect[1])
        # Return to main menu
        self.mainmenu_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Main Menu')
        btn_rect = self.mainmenu_btn.getRect().width, self.mainmenu_btn.getRect().height
        self.mainmenu_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H - btn_rect[1] / 2
                                 + btn_rect[1] * 2)

    def change_online_state(self, next_state):
        self.curr_state = self.states[next_state]
        self.curr_state.enter_state()

    def enter_state(self):
        self.curr_state = self.states["self"]
