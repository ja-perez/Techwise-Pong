import pygame
import sys
from Constants import *
from states.menus.mainmenu import MainMenu
from states.modes.local import Local
from states.state import State

# States = Dict()

class Game():
    def __init__(self):
        # Pygame initializations
        pygame.init()
        self.game_canvas = pygame.Surface((GAME_W, GAME_H))
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.running = True
        self.clock = pygame.time.Clock()

        self.states = {"mainmenu": MainMenu(self, "mainmenu"), "local": Local(self, "local")}
        self.curr_state = self.states["mainmenu"]

        # input handler using input_handler class
        # global States
        # States.update({"MainMenu": MainMenuState()})
        # States.update({})

    def update(self):
        # self.get_dt()
        # self.ih.handle_input()    call to input handler
        # for command, arg
        # CommandQueue = self.current_state.input_handler.handle_input()
        # for command, args in CommandQueue:
        #    command.execute(self, args)

        #######################
        # temp input handling #
        if pygame.event.peek(pygame.QUIT):
            self.running = False
        # temp input handling #
        #######################

        self.curr_state.update()
        self.temp_render()
        self.clock.tick(60)

    def change_state(self, next_state: State):
        # WIP - called from command and passed next state string
        self.curr_state.exit_state()
        self.curr_state = self.states[next_state.state_name()]
        self.curr_state.enter_state()
        # self.input_handler = curr_state.input_handler

    ####################
    # temp render method
    def temp_render(self):
        self.screen.blit(pygame.transform.scale(self.game_canvas, (WIN_W, WIN_H)), (0, 0))
        self.curr_state.render()
        pygame.display.flip()
    # temp render method
    ####################

    def teardown(self):
        # handle game exit
        self.curr_state.exit_state()
        pygame.quit()
        sys.exit()
