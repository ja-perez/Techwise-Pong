from ecs.entity import Entity
from ecs.components import *
from Constants import *
import pygame


class Player(Entity):
    def __init__(self, name, x, y):
        Entity.__init__(self, name)
        self.score = 0
        self.surface = pygame.Surface(PADDLE)
        self.surface.fill(WHITE)
        self.components["graphics"] = GraphicComponent(self.surface, x, y)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)


class Ball(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
