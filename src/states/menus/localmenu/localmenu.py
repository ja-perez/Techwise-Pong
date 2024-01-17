import pygwidgets
import pygame
from states.state import State
from ecs.entities import State_Text
from Constants import *


class LocalMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.mode_btns, self.player_btns = [], []
        self.mode_bool = False
        self.create_texts()
        self.create_mode_buttons()
        self.create_player_buttons()
        self.return_state = ""

    def update(self):
        for event in pygame.event.get():
            if not self.mode_bool:
                self.disable_player_btns()
                self.enable_mode_btns()
                if self.classic_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(0)
                    self.mode_bool = True
                    # change to local with classic setting
                if self.frenzy_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(1)
                    self.mode_bool = True
                    # change to local with frenzy setting
                if self.low_grav_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(2)
                    self.mode_bool = True
                    # change to local with low grav setting
                if self.through_the_ages_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(3)
                    self.mode_bool = True
                    # change to local with through the ages setting
            else:
                self.enable_player_btns()
                self.disable_mode_btns()
                if self.p_vs_p_btn.handleEvent(event):

                    self.game.states["local"].set_player_pair(0)
                    self.change_state("local")
                if self.p_vs_ai_btn.handleEvent(event):
                    self.game.states["local"].set_player_pair(1)
                    self.change_state("local")
                if self.ai_vs_ai_btn.handleEvent(event):
                    self.game.states["local"].set_player_pair(2)
                    self.change_state("local")

            if self.return_button.handleEvent(event):
                self.change_state(self.return_state)

    def render(self):
        if not self.mode_bool:
            self.game.screen.blit(self.choose_mode_text.components["graphics"].surface,
                                  self.choose_mode_text.components["graphics"].rect)
        else:
            self.game.screen.blit(self.choose_players_text.components["graphics"].surface,
                                  self.choose_players_text.components["graphics"].rect)
        self.button_display()

    def create_texts(self):
        self.choose_mode_text = State_Text("Choose A Game Mode", TEXT_SIZE, WHITE, FONT_NAME)
        self.choose_mode_text.set_pos(GAME_W - self.choose_mode_text.get_size()[0] // 2, GAME_H / 2.5)
        self.choose_players_text = State_Text("Choose Player Setting", TEXT_SIZE, WHITE, FONT_NAME)
        self.choose_players_text.set_pos(GAME_W - self.choose_players_text.get_size()[0] // 2, GAME_H / 2.5)

    def enable_mode_btns(self):
        for btn in self.mode_btns:
            btn.enable()

    def disable_mode_btns(self):
        for btn in self.mode_btns:
            btn.disable()

    def enable_player_btns(self):
        for btn in self.player_btns:
            btn.enable()

    def disable_player_btns(self):
        for btn in self.player_btns:
            btn.disable()

    def button_display(self):
        for btn in self.mode_btns:
            btn.draw()
        for btn in self.player_btns:
            btn.draw()
        self.return_button.draw()

    def create_mode_buttons(self):
        height_variable = 40
        width_variable = 150
        x_pos = WIN_W // 3 - width_variable // 2
        y_pos = WIN_H // 2 - height_variable // 2 + height_variable * 2
        self.classic_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Classic',
                                                    fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                    width=width_variable)
        self.classic_button.moveXY(x_pos, y_pos - height_variable * 4)

        self.frenzy_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Frenzy',
                                                   fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                   width=width_variable)
        self.frenzy_button.moveXY(x_pos, y_pos - height_variable * 3)

        self.low_grav_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Low Gravity',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable)
        self.low_grav_button.moveXY(x_pos, y_pos - height_variable * 2)

        self.through_the_ages_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Through the Ages',
                                                             fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                             width=width_variable)
        self.through_the_ages_button.moveXY(x_pos, y_pos - height_variable)

        self.mode_btns = [self.classic_button, self.frenzy_button,
                          self.low_grav_button, self.through_the_ages_button]

    def create_player_buttons(self):
        height_variable = 40
        width_variable = 150
        x_pos = WIN_W * 2 // 3 - width_variable // 2
        y_pos = WIN_H // 2 - height_variable // 2 + height_variable
        self.p_vs_p_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Player vs Player',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable, height=height_variable)
        self.p_vs_p_btn.moveXY(x_pos, y_pos - height_variable * 3)

        self.p_vs_ai_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Player vs AI',
                                                  fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                  width=width_variable)
        self.p_vs_ai_btn.moveXY(x_pos, y_pos - height_variable * 2)

        self.ai_vs_ai_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'AI vs AI',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable)
        self.ai_vs_ai_btn.moveXY(x_pos, y_pos - height_variable)

        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return',
                                                   fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                   width=width_variable)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                  WIN_H / 2 - self.return_button.getRect().height / 2 + height_variable * 2)

        self.player_btns = [self.p_vs_p_btn, self.p_vs_ai_btn, self.ai_vs_ai_btn]

    def enter_state(self, prev_state):
        self.return_state = prev_state

    def exit_state(self):
        self.mode_bool = False
