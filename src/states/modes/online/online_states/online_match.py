from states.state import State
from Constants import *

class Online_Match(State):
    def __init__(self, game, online):
        State.__init__(self, game)
        self.online = online
        self.curr_match = None

    def update(self, state):
        pass

    def render(self):
        print(self.curr_match)

    def enter_state(self):
        self.curr_match = self.online.network.send("join_public")

    def exit_state(self):
        pass