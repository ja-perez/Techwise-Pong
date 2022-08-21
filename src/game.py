import pygame
import sys
from Constants import *
from states.menus.mainmenu.mainmenu import MainMenu
from states.menus.settings.settings import Settings
from states.menus.graphicsmenu.graphicsmenu import GraphicsMenu
from states.menus.settings.update_set import Change_Graphics, Change_Audio, Change_Controls
from states.menus.pause.pause import Pause
from states.modes.local.local import Local
from states.menus.localmenu.localmenu import LocalMenu
from states.modes.online.online import Online
from pygame import mixer
from themes.themes import Themes
import random

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
                       "settings": Settings(self, "settings"), "pause": Pause(self, "pause"),
                       "localmenu": LocalMenu(self, "localmenu"),
                       "graphicsmenu": GraphicsMenu(self, "graphicsmenu"), "audio": Change_Audio(self, "audio"),
                       "controls": Change_Controls(self, "controls"), "online": Online(self, "online")}
        self.curr_state = self.states["mainmenu"]
        self.change_music()

        if not self.states["local"].classic_bool:
            self.background = pygame.image.load(self.states["local"].themes.background_color)
        else:
            self.background = self.states["local"].background_color


    def change_music(self):
        # Background Music
        mixer.music.load(self.states["local"].themes.background_music)
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)

    def change_background_color(self, background_color ):
        self.game_canvas.fill(random.choices(range(256), k=3))

    def update(self):
        if pygame.event.peek(pygame.QUIT):
            self.running = False
        self.curr_state.update()
        self.render()
        self.clock.tick(60)

    def render(self):
        self.reset_screen()
        self.curr_state.render()
        pygame.display.flip()

    def reset_screen(self):

        if self.states["local"].classic_bool:
            self.screen.blit(pygame.transform.scale(self.game_canvas, (WIN_W, WIN_H)), (0, 0))
        else:
            self.screen.blit(pygame.transform.scale(self.background, (WIN_W, WIN_H)), (0, 0))

    def teardown(self):
        # handle game exit
        self.curr_state.exit_state()
        pygame.quit()
        sys.exit()
