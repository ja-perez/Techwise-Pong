import pygwidgets
import pygame
from states.state import State
from Constants import *

class LocalMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_buttons()
        self.return_state = ""

    def update(self):
        for event in pygame.event.get():
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

    def button_display(self):
        self.graphics_button.draw()
        self.audio_button.draw()
        self.controls_button.draw()
        self.return_button.draw()

    def create_buttons(self):
        height_variable = 80
        self.graphics_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Player vs Player',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME)
        button_height = self.graphics_button.getRect().height
        self.graphics_button.moveXY(WIN_W / 2 - self.graphics_button.getRect().width / 2,
                                    WIN_H / 2 - self.graphics_button.getRect().height / 2
                                    - button_height * 3 + height_variable)

        self.audio_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Player vs AI',
                                                  fontSize=MENU_FONT_SIZE, fontName=FONT_NAME)
        self.audio_button.moveXY(WIN_W / 2 - self.audio_button.getRect().width / 2,
                                    WIN_H / 2 - self.audio_button.getRect().height / 2
                                 - button_height * 2 + height_variable)
        self.controls_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'AI vs AI',
                                                     fontSize=MENU_FONT_SIZE, fontName=FONT_NAME)
        self.controls_button.moveXY(WIN_W / 2 - self.controls_button.getRect().width / 2,
                                    WIN_H / 2 - self.controls_button.getRect().height / 2
                                    - button_height + height_variable)
        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return',
                                                   fontSize=MENU_FONT_SIZE, fontName=FONT_NAME)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                    WIN_H / 2 - self.return_button.getRect().height / 2 + height_variable)

    def enter_state(self, prev_state):
        self.return_state = prev_state
