import pygwidgets
import pygame
from states.state import State
from Constants import *


class MainMenuSettings(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.create_buttons()

    def update(self):
        for event in pygame.event.get():
            if self.graphics_button.handleEvent(event):
                self.change_state("mmgraphics")
            if self.audio_button.handleEvent(event):
                self.change_state("mmaudio")
            if self.controls_button.handleEvent(event):
                self.change_state("mmcontrols")
            if self.return_button.handleEvent(event):
                self.change_state("mainmenu")

    def render(self):
        self.button_display()

    def button_display(self):
        self.graphics_button.draw()
        self.audio_button.draw()
        self.controls_button.draw()
        self.return_button.draw()

    def create_buttons(self):
        self.graphics_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Graphics', fontSize=45)
        button_height = self.graphics_button.getRect().height
        self.graphics_button.moveXY(WIN_W / 2 - self.graphics_button.getRect().width / 2,
                                    WIN_H / 2 - self.graphics_button.getRect().height / 2
                                    - button_height * 3)

        self.audio_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Audio', fontSize=45)
        self.audio_button.moveXY(WIN_W / 2 - self.audio_button.getRect().width / 2,
                                    WIN_H / 2 - self.audio_button.getRect().height / 2
                                 - button_height * 2)
        self.controls_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Controls', fontSize=45)
        self.controls_button.moveXY(WIN_W / 2 - self.controls_button.getRect().width / 2,
                                    WIN_H / 2 - self.controls_button.getRect().height / 2
                                    - button_height)
        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return', fontSize=45)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                    WIN_H / 2 - self.return_button.getRect().height / 2)

class MMGraphics():
    def __init__(self, game):
        State.__init__(self, game)

class MMAudio():
    def __init__(self, game):
        State.__init__(self, game)

class MMControls():
    def __init__(self, game):
        State.__init__(self, game)
