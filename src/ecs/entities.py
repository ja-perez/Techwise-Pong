from ecs.entity import Entity
from ecs.components import *
from Constants import *
import pygame


class Player(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.score = 0
        self.surface = pygame.Surface(PADDLE)
        self.surface.fill(WHITE)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.components["velocity"] = VelocityComponent(0, 0)

    def get_name(self):
        return self.name

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def get_score(self):
        return str(self.score)

    def increase_score(self, increment):
        self.score += increment


class Ball(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.surface = pygame.Surface(BALL)
        self.surface.fill(WHITE)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.components["velocity"] = VelocityComponent(0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def x_vel(self):
        return self.components["velocity"].x_velocity

    def y_vel(self):
        return self.components["velocity"].y_velocity


class Score(Entity):
    def __init__(self, title, size, color):
        Entity.__init__(self, title)
        self.color = color
        self.size = size
        self.components["text"] = TextComponent(title, size, color)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def update_surface(self):
        self.surface = self.components["text"].font.render(self.name, False, self.color)

    def update_graphics(self):
        self.update_surface()
        self.components["graphics"].surface = self.surface

class Pause(Entity):
    def __init__(self, title, size, color):
        Entity.__init__(self, title)
        self.components["text"] = TextComponent(title, size, color)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

class Start(Entity):
    def __init__(self, title, size, color):
        Entity.__init__(self, title)
        self.components["text"] = TextComponent(title, size, color)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)
