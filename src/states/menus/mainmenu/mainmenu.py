import pygwidgets
import pygame
from states.state import State
from Constants import *
from commands.command import *
from input.input_handler import *


class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.create_buttons()

    def update(self):
        for event in pygame.event.get():
            if self.local_game_button.handleEvent(event):
                self.change_state("local")
            if self.online_game_button.handleEvent(event):
                self.change_state("online")
            if self.mainmenu_settings.handleEvent(event):
                self.change_state("mmsettings")
            if self.exit_button.handleEvent(event):
                print("Goodbye")
                self.game.running = False

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
        self.online_game_button.draw()
        self.mainmenu_settings.draw()
        self.exit_button.draw()

    def create_buttons(self):
        self.local_game_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Local')
        button_height = self.local_game_button.getRect().height
        self.local_game_button.moveXY(WIN_W / 2 - self.local_game_button.getRect().width / 2,
                                      WIN_H / 2 - self.local_game_button.getRect().height / 2
                                      + button_height)
        self.online_game_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Online')
        self.online_game_button.moveXY(WIN_W / 2 - self.online_game_button.getRect().width / 2,
                                      WIN_H / 2 - self.online_game_button.getRect().height / 2
                                      + button_height * 2)
        self.mainmenu_settings = pygwidgets.TextButton(self.game.screen, (0, 0), 'Settings')
        self.mainmenu_settings.moveXY(WIN_W / 2 - self.mainmenu_settings.getRect().width / 2,
                                      WIN_H / 2 - self.mainmenu_settings.getRect().height / 2
                                      + button_height * 3)
        self.exit_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Exit Game')
        self.exit_button.moveXY(WIN_W / 2 - self.exit_button.getRect().width / 2,
                                WIN_H / 2 - self.exit_button.getRect().height / 2
                                + button_height * 4)

    def exit_state(self):
        pass

    def enter_state(self):
        pass
