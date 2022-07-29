import pygwidgets
import pygame
from states.state import State
from Constants import *
from states.menus.pause.pausecommands import PauseCommand, toggle_pause


class Pause(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_buttons()


    def update(self):
        for event in pygame.event.get():
            if self.resume_button.handleEvent(event):
                self.change_state("local")
            if self.settings_button.handleEvent(event):
                self.change_state("mmsettings")
            if self.exit_to_mainmenu.handleEvent(event):
                self.change_state("mainmenu")
            if self.exit_to_desktop.handleEvent(event):
                print("Goodbye")
                self.game.running = False


    # def register_commands(self):
    #     # Command: press p to pause and transition to pause state
    #     self.pause_command = PauseCommand(ActiveOn.PRESSED, toggle_pause, self)
    #     self.ih.register_command(pygame.K_p, self.pause_command)

    def render(self):
        #self.pause_display()
        self.test_display()
        self.button_display()

    def test_display(self):
        text_surface = self.game.font.render("pause screen works", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (GAME_W, GAME_H / 2.5)
        self.game.screen.blit(text_surface, text_rect)

    def button_display(self):
        self.resume_button.draw()
        self.settings_button.draw()
        self.exit_to_mainmenu.draw()
        self.exit_to_desktop.draw()

    def create_buttons(self):
        self.resume_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Resume', fontSize=45)
        button_height = self.resume_button.getRect().height
        self.resume_button.moveXY(WIN_W / 2 - self.resume_button.getRect().width / 2,
                                    WIN_H / 2 - self.resume_button.getRect().height / 2
                                    - button_height * 3)

        self.settings_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Settings', fontSize=45)
        self.settings_button.moveXY(WIN_W / 2 - self.settings_button.getRect().width / 2,
                                 WIN_H / 2 - self.settings_button.getRect().height / 2
                                 - button_height * 2)
        self.exit_to_mainmenu = pygwidgets.TextButton(self.game.screen, (0, 0), 'Exit to Main Menu', fontSize=45)
        self.exit_to_mainmenu.moveXY(WIN_W / 2 - self.exit_to_mainmenu.getRect().width / 2,
                                    WIN_H / 2 - self.exit_to_mainmenu.getRect().height / 2
                                    - button_height)
        self.exit_to_desktop = pygwidgets.TextButton(self.game.screen, (0, 0), 'Exit to Desktop', fontSize=45)
        self.exit_to_desktop.moveXY(WIN_W / 2 - self.exit_to_desktop.getRect().width / 2,
                                  WIN_H / 2 - self.exit_to_desktop.getRect().height / 2)

    def exit_state(self):
        pass
    def enter_state(self):
        pass