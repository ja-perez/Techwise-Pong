import pygwidgets
import pygame
from states.state import State
from Constants import *


class Change_Graphics(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)

    def render(self):
        pass

class Change_Audio(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)

    def render(self):
        pass

class Change_Controls(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)

    def render(self):
        pass
