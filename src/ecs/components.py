import pygame
from Constants import *


class GraphicComponent:
    def __init__(self, surface, initial_x, initial_y):
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.rect.move(initial_x, initial_y)


class VelocityComponent:
    def __init__(self, x_velocity, y_velocity):
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity


class AudioComponent:
    def __init__(self, sound: pygame.mixer.Sound):
        self.sound = sound


class TextComponent:
    def __init__(self, text, size, color):
        self.text = text
        self.size = size
        self.color = color
