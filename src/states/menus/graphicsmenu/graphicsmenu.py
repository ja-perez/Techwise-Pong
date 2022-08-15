import pygwidgets
import pygame
from states.state import State
from Constants import *
from commands.command import *
from input.input_handler import *
from ecs.entities import Player

class GraphicsMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_left_buttons()
        self.create_return_button()
        self.create_right_buttons()
        self.return_state = ""
        self.left_paddle_color = WHITE
        self.right_paddle_color = WHITE


    def get_left_paddle_color(self):
        return self.left_paddle_color

    def update(self):
        for event in pygame.event.get():
            if self.left_blue_button.handleEvent(event):
                self.left_paddle_color = BLUE
                self.game.states["local"].set_left_paddle_color(BLUE)
            if self.left_green_button.handleEvent(event):
                self.left_paddle_color = GREEN
                self.game.states["local"].set_left_paddle_color(GREEN)
            if self.left_red_button.handleEvent(event):
                self.left_paddle_color = RED
                self.game.states["local"].set_left_paddle_color(RED)
            if self.left_yellow_button.handleEvent(event):
                self.left_paddle_color = YELLOW
                self.game.states["local"].set_left_paddle_color(YELLOW)
            if self.left_white_button.handleEvent(event):
                self.left_paddle_color = WHITE
                self.game.states["local"].set_left_paddle_color(WHITE)

            if self.right_blue_button.handleEvent(event):
                self.right_paddle_color = BLUE
                self.game.states["local"].set_right_paddle_color(BLUE)
            if self.right_green_button.handleEvent(event):
                self.right_paddle_color = GREEN
                self.game.states["local"].set_right_paddle_color(GREEN)
            if self.right_red_button.handleEvent(event):
                self.right_paddle_color = RED
                self.game.states["local"].set_right_paddle_color(RED)
            if self.right_yellow_button.handleEvent(event):
                self.right_paddle_color = YELLOW
                self.game.states["local"].set_right_paddle_color(YELLOW)
            if self.right_white_button.handleEvent(event):
                self.right_paddle_color = WHITE
                self.game.states["local"].set_right_paddle_color(WHITE)

            if self.return_button.handleEvent(event):
                self.change_state("local")

    def render(self):
        self.button_display()
        self.player1_text()
        self.player2_text()
        self.create_left_paddle(self.left_paddle_color)
        self.create_right_paddle(self.right_paddle_color)

    def create_left_paddle(self, color):
        self.surface = pygame.Surface((60,200))
        self.surface.fill(color)
        self.game.screen.blit(self.surface, (50,WIN_H//3 + 20))


    def create_right_paddle(self, color):
        self.surface = pygame.Surface((60, 200))
        self.surface.fill(color)
        self.game.screen.blit(self.surface, ((WIN_W - 100), WIN_H / 3 + 20))

    def player1_text(self):
        font = pygame.font.Font(FONT_NAME, 30)
        text_surface = font.render("Player 1 Settings", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (GAME_W/3, GAME_H / 2.5)
        self.game.screen.blit(text_surface, text_rect)

    def player2_text(self):
        font = pygame.font.Font(FONT_NAME, 30)
        text_surface = font.render("Player 2 Settings", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (GAME_W/3 * 5, GAME_H / 2.5)
        self.game.screen.blit(text_surface, text_rect)

    def button_display(self):
        self.left_blue_button.draw()
        self.left_green_button.draw()
        self.left_red_button.draw()
        self.left_yellow_button.draw()
        self.left_white_button.draw()

        self.right_blue_button.draw()
        self.right_green_button.draw()
        self.right_red_button.draw()
        self.right_yellow_button.draw()
        self.right_white_button.draw()

        self.return_button.draw()

# Button pixel: 35 x 35 pixels
    def create_left_buttons(self):
        height_var = 35
        self.left_blue_button = pygwidgets.CustomButton(self.game.screen, (WIN_W/4, WIN_H/4 + height_var),
                                                   'color_buttons/blue.png')

        self.left_green_button = pygwidgets.CustomButton(self.game.screen, (WIN_W/4, WIN_H/4 + 3*height_var),
                                                   'color_buttons/green.png')

        self.left_red_button = pygwidgets.CustomButton(self.game.screen, (WIN_W / 4, WIN_H / 4 + 5*height_var),
                                                    'color_buttons/red.png')

        self.left_yellow_button = pygwidgets.CustomButton(self.game.screen, (WIN_W / 4, WIN_H / 4 + 7*height_var),
                                                    'color_buttons/yellow.png')

        self.left_white_button = pygwidgets.CustomButton(self.game.screen, (WIN_W / 4, WIN_H / 4 + 9 * height_var),
                                                     'color_buttons/white.png')

    def create_right_buttons(self):
        height_var = 35
        self.right_blue_button = pygwidgets.CustomButton(self.game.screen, ((WIN_W / 4 + WIN_W/2), WIN_H / 4 + height_var),
                                                   'color_buttons/blue.png')

        self.right_green_button = pygwidgets.CustomButton(self.game.screen, ((WIN_W / 4 + WIN_W/2), WIN_H / 4 + 3 * height_var),
                                                    'color_buttons/green.png')

        self.right_red_button = pygwidgets.CustomButton(self.game.screen, ((WIN_W / 4 + WIN_W/2), WIN_H / 4 + 5 * height_var),
                                                  'color_buttons/red.png')

        self.right_yellow_button = pygwidgets.CustomButton(self.game.screen, ((WIN_W / 4 + WIN_W/2), WIN_H / 4 + 7 * height_var),
                                                     'color_buttons/yellow.png')

        self.right_white_button = pygwidgets.CustomButton(self.game.screen, ((WIN_W / 4 + WIN_W/2), WIN_H / 4 + 9 * height_var),
                                                    'color_buttons/white.png')


    def create_return_button(self):
        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return', fontSize=45, fontName= FONT_NAME)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                  WIN_H / 2 - self.return_button.getRect().height + 100)

    def enter_state(self, prev_state):
        self.return_state = prev_state
