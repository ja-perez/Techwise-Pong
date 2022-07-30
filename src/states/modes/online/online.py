from states.state import State
from states.modes.online.network import Network


class Online(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self):
        pass

    def render(self):
        pass

    def enter_state(self):
        self.network = Network()
        if not self.network.getP():
            print("Connection Failed")
