import pygame
import sys
from Constants import *
from states.menus.mainmenu import MainMenu
from states.modes.local import Local
from states.settings.mmset import MainMenuSettings
from states.state import State


class Game():
    def __init__(self):
        # Pygame/GUI specific initializations
        pygame.init()
        self.game_canvas = pygame.Surface((GAME_W, GAME_H))
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.running = True
        self.clock = pygame.time.Clock()

        # Pong game states initializations
        self.states = {"mainmenu": MainMenu(self, "mainmenu"), "local": Local(self, "local"),
                       "mmsettings": MainMenuSettings(self, "mmsettings")}
        self.curr_state = self.states["mainmenu"]

    def update(self):
        #######################
        # temp input handling #
        if pygame.event.peek(pygame.QUIT):
            self.running = False
        # temp input handling #
        #######################

        self.curr_state.update()
        self.temp_render()
        self.clock.tick(60)

    ######################
    # temp render method #
    def temp_render(self):
        self.screen.blit(pygame.transform.scale(self.game_canvas, (WIN_W, WIN_H)), (0, 0))
        self.curr_state.render()
        pygame.display.flip()
    # temp render method #
    ######################

    def teardown(self):
        # handle game exit
        self.curr_state.exit_state()
        pygame.quit()
        sys.exit()
