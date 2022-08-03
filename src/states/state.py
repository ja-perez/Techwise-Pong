from commands.command import *
from input.input_handler import InputHandler


class State():
    def __init__(self, game, name=""):
        self.game = game
        self.name = name
        self.ih = InputHandler()

    def get_name(self):
        return self.name

    def update(self):
        pass

    def render(self, surface):
        pass

    def register_commands(self):
        pass

    def change_state(self, next_state, prev_state=""):
        self.exit_state()
        self.game.curr_state = self.game.states[next_state]
        if prev_state:
            self.game.curr_state.enter_state(prev_state)
        else:
            self.game.curr_state.enter_state()

    def exit_state(self):
        pass

    def enter_state(self, prev_state=""):
        pass
