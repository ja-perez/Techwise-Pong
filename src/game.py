import os
import pygame
from Constants import *
from states.title import Title

# Input testing
# from input.input_handler import *
# from commands.command import *


class Game():
    def __init__(self):
        # Pygame initializations
        pygame.init()
        self.game_canvas = pygame.Surface((GAME_W, GAME_H))
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

        # Game Loop initializations
        self.running, self.playing = True, True
        self.state_stack = []
        self.load_states()
        # self.load_input_handler()
        self.clock = pygame.time.Clock()

    def game_loop(self):

        while self.playing:
            # self.get_dt()
            # self.get_events()
            # self.ih.handle_input()
            if pygame.event.peek(pygame.QUIT):
                # logging.shutdown()
                self.playing = False
                pygame.quit()
            self.update()
            self.render()
            self.clock.tick(60)

    def update(self):
        pass
        # self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (WIN_W, WIN_H)), (0, 0))
        pygame.display.flip()

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)


"""
    def load_input_handler(self):
        s = SelectCommand(ActiveOn.RELEASED)
        self.ih = InputHandler()
        self.register_command(pygame.K_ESCAPE, s)
"""

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
