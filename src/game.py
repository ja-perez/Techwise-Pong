import pygame
import sys
from Constants import *
from states.modes.local.local import Local
from states.menus.mainmenu.mainmenu import MainMenu
from states.menus.mainmenu.mmsettings import MainMenuSettings, MMGraphics, MMAudio, MMControls
from states.menus.pause.pause import Pause


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
                       "mmsettings": MainMenuSettings(self, "mmsettings"), "pause": Pause(self, "pause"),
                       "mmgraphics": MMGraphics(self, "mmgraphics"), "mmaudio": MMAudio(self, "mmaudio"),
                       "mmcontrols": MMControls(self, "mmcontrols")}
        self.curr_state = self.states["mainmenu"]

    def update(self):
        if pygame.event.peek(pygame.QUIT):
            self.running = False
        self.curr_state.update()
        self.render()
        self.clock.tick(60)

    def render(self):
        self.screen.blit(pygame.transform.scale(self.game_canvas, (WIN_W, WIN_H)), (0, 0))
        self.curr_state.render()
        pygame.display.flip()

    def teardown(self):
        # handle game exit
        self.curr_state.exit_state()
        pygame.quit()
        sys.exit()
