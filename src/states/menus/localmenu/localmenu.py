import pygwidgets
import pygame
from states.state import State
from Constants import *


class LocalMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.mode_btns, self.player_btns = [], []
        self.mode_bool = False
        self.create_mode_buttons()
        self.create_player_buttons()
        self.return_state = ""

    def update(self):
        for event in pygame.event.get():
            if not self.mode_bool:
                self.disable_player_btns()
                self.enable_mode_btns()
                if self.classic_button.handleEvent(event):
                    self.mode_bool = True
                if self.frenzy_button.handleEvent(event):
                    self.mode_bool = True
                if self.low_grav_button.handleEvent(event):
                    self.mode_bool = True
                if self.through_the_ages_button.handleEvent(event):
                    self.mode_bool = True
            else:
                self.enable_player_btns()
                self.disable_mode_btns()
                if self.graphics_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(0)
                    self.change_state("local")
                if self.audio_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(1)
                    self.change_state("local")
                if self.controls_button.handleEvent(event):
                    self.game.states["local"].set_game_mode(2)
                    self.change_state("local")

            if self.return_button.handleEvent(event):
                self.change_state(self.return_state)

    def render(self):
        self.state_text_display()
        self.button_display()

    def state_text_display(self):
        font = pygame.font.Font(FONT_NAME, TEXT_SIZE)
        text_surface = font.render("Local Menu", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (GAME_W, GAME_H / 2.5)
        self.game.screen.blit(text_surface, text_rect)

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
        self.graphics_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Player vs Player',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable, height=height_variable)
        button_height = self.graphics_button.getRect().height
        self.graphics_button.moveXY(x_pos, y_pos - height_variable * 3)

        self.audio_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Player vs AI',
                                                  fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                  width=width_variable)
        self.audio_button.moveXY(x_pos, y_pos - height_variable * 2)

        self.controls_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'AI vs AI',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable)
        self.controls_button.moveXY(x_pos, y_pos - height_variable)

        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return',
                                                   fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                   width=width_variable)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                  WIN_H / 2 - self.return_button.getRect().height / 2 + height_variable * 2)

        self.player_btns = [self.graphics_button, self.audio_button, self.controls_button]

    def enter_state(self, prev_state):
        self.return_state = prev_state

    def exit_state(self):
        self.mode_bool = False
