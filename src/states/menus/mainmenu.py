import pygwidgets
import pygame
from states.state import State
from Constants import *


class MainMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_buttons()

    #######################
    # temp button methods #
    def create_buttons(self):
        self.play_game_button = pygwidgets.TextButton(self.game.screen, (GAME_W - 40, GAME_H), 'Player vs. Player')
        self.exit_button = pygwidgets.TextButton(self.game.screen, (GAME_W - 34, GAME_H + 50), 'Exit Game')
    # temp button methods #
    #######################

    def update(self):
        #######################
        # temp input handling #
        for event in pygame.event.get():
            if self.play_game_button.handleEvent(event):
                print("Playing game and having fun!")
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
        self.play_game_button.draw()
        self.exit_button.draw()
    # temp render methods #
    #######################
