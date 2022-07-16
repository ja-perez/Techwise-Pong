from states.state import State
from Constants import *


class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.title_options = {"Player vs. Player": 0, "Exit": 1}

    def update(self):
        pass

    def render(self, display):
        display.fill(BLACK)
        self.game.draw_text(display, GAME_TITLE, WHITE, GAME_W / 2, GAME_H / 4)
