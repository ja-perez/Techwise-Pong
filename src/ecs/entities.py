from ecs.entity import Entity
from ecs.components import *
from Constants import *
import pygame


class Player(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.score = 0
        self.paddle_width = PADDLE_W
        self.paddle_height = PADDLE_H
        self.surface = pygame.Surface((self.paddle_width, self.paddle_height))
        self.surface.fill(WHITE)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.components["velocity"] = VelocityComponent(0, 0)
        self.e_type = "Player"
        # self.change_size(1, 2)

    def set_color(self, color):
        self.surface.fill(color)

    def change_size(self, width, height):
        self.paddle_width += width
        self.paddle_height = height

    def get_size(self):
        return self.paddle_width, self.paddle_height

    def set_cords(self, x, y):
        self.components["graphics"].rect.topleft = (x, y)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def get_score(self):
        return str(self.score)

    def increase_score(self, increment):
        self.score += increment

    def get_y_vel(self):
        return self.components["velocity"].y_velocity

class Ball(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.surface = pygame.Surface(BALL)
        # THIS DOESNT WORK?
        # self.surface.fill(YELLOW)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.components["graphics"].is_circle = True
        self.components["graphics"].radius = BALL_RADIUS
        self.components["graphics"].color = WHITE
        self.components["velocity"] = VelocityComponent(0, 0)
        self.e_type = "Ball"

    def set_color(self, color):
        self.components["graphics"].color = color

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def set_cords(self, x, y):
        self.components["graphics"].rect.topleft = (x, y)

    def increase_radius(self, num):
        self.components["graphics"].radius += num

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def x_vel(self):
        return self.components["velocity"].x_velocity

    def y_vel(self):
        return self.components["velocity"].y_velocity

    def get_cords(self):
        return self.components["graphics"].rect.center


class Score(Entity):
    def __init__(self, title, size, color, font_name=None):
        Entity.__init__(self, title)
        self.color = color
        self.size = size
        self.components["text"] = TextComponent(title, size, color, font_name)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.e_type = "Score"

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def update_surface(self):
        self.surface = self.components["text"].font.render(self.name, False, self.color)

    def update_graphics(self):
        self.update_surface()
        self.components["graphics"].surface = self.surface


class Pause(Entity):
    def __init__(self, title, size, color, fontName=None):
        Entity.__init__(self, title)
        self.components["text"] = TextComponent(title, size, color, fontName)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)


class Start(Entity):
    def __init__(self, title, size, color, fontName=None):
        Entity.__init__(self, title)
        self.components["text"] = TextComponent(title, size, color, fontName)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)


class State_Text(Entity):
    def __init__(self, title, size, color, fontName=None):
        Entity.__init__(self, title)
        self.color = color
        self.size = size
        self.components["text"] = TextComponent(title, size, color, fontName)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.e_type = "State_Text"

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def get_size(self):
        return self.components["graphics"].rect.width, self.components["graphics"].rect.height

    def update_surface(self):
        self.surface = self.components["text"].font.render(self.name, False, self.color)

    def update_graphics(self):
        self.update_surface()
        self.components["graphics"].surface = self.surface

    def set_coords(self, x, y):
        self.components["graphics"].rect.center = x, y

    def get_width(self):
        return self.components["graphics"].rect.width