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

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def get_score(self):
        return str(self.score)

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

class Score(Entity):
    def __init__(self, title, size, color):
        Entity.__init__(self, title)
        self.components["text"] = TextComponent(title, size, color)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)
