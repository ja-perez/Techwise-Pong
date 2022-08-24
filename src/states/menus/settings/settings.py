import pygwidgets
import pygame
from states.state import State
from Constants import *


class Settings(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_buttons()
        self.return_state = ""

    def update(self):
        for event in pygame.event.get():
            if self.graphics_button.handleEvent(event):
                self.change_state("graphicsmenu", self.name)
            if self.audio_button.handleEvent(event):
                self.change_state("audiomenu", self.name)
            if self.controls_button.handleEvent(event):
                self.change_state("controls")
            if self.return_button.handleEvent(event):
                self.change_state(self.return_state)

    def render(self):
        self.state_text_display()
        self.button_display()

    def state_text_display(self):
        font = pygame.font.Font(FONT_NAME, TEXT_SIZE)
        text_surface = font.render("Settings Menu", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (GAME_W, GAME_H / 2.5)
        self.game.screen.blit(text_surface, text_rect)

    def button_display(self):
        self.graphics_button.draw()
        self.audio_button.draw()
        # self.controls_button.draw()
        self.return_button.draw()

    def create_buttons(self):
        height_variable = 45
        width_variable = 100
        self.graphics_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Graphics',
                                                       fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable, height=height_variable)
        button_height = self.graphics_button.getRect().height
        self.graphics_button.moveXY(GAME_W - width_variable / 2, GAME_H - height_variable / 2)

        self.audio_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Audio',
                                                       fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable, height=height_variable)
        self.audio_button.moveXY(GAME_W - width_variable / 2, GAME_H - height_variable / 2
                                 + height_variable)
        self.controls_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Controls',
                                                       fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable, height=height_variable)
        self.controls_button.moveXY(GAME_W - width_variable / 2, GAME_H - height_variable / 2
                                    + height_variable * 2)
        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return',
                                                       fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                     width=width_variable, height=height_variable)
        self.return_button.moveXY(GAME_W - width_variable / 2, GAME_H - height_variable / 2
                                  + height_variable * 2)

    def enter_state(self, prev_state=""):
        if prev_state:
            self.return_state = prev_state
