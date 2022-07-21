import pygwidgets
import pygame
from states.state import State
from Constants import *

from states.modes.local import Local

class MainMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_buttons()

    ######################
    # temp button method #
    def create_buttons(self):
        self.local_game_button = pygwidgets.TextButton(self.game.screen, (GAME_W - 40, GAME_H), 'Local')
        self.mainmenu_options = pygwidgets.TextButton(self.game.screen, (GAME_W - 34, GAME_H + 50), 'Settings')
        self.exit_button = pygwidgets.TextButton(self.game.screen, (GAME_W - 34, GAME_H + 100), 'Exit Game')
    # temp button method #
    ######################

    def update(self):
        #######################
        # temp input handling #
        for event in pygame.event.get():
            if self.local_game_button.handleEvent(event):
                print("Playing game and having fun")
                self.game.change_state("local")
            if self.exit_button.handleEvent(event):
                print("Goodbye")
                self.game.running = False
        # temp input handling #
        #######################

    #######################
    # temp render methods #
    def render(self):
        self.title_display()
        self.button_display()

    def title_display(self):
        text_surface = self.game.font.render(GAME_TITLE, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (GAME_W, GAME_H / 2.5)
        self.game.screen.blit(text_surface, text_rect)

    def button_display(self):
        self.local_game_button.draw()
        self.mainmenu_options.draw()
        self.exit_button.draw()
    # temp render methods #
    #######################
