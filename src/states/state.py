class State():
    def __init__(self, game, name):
        self.game = game
        self.name = name

    def update(self):
        # input handler
        pass

    def render(self, surface):
        pass

    def state_name(self):
        return self.name

    def change_state(self, next_state):
        self.exit_state()
        self.game.curr_state = self.game.states[next_state]
        self.enter_state()

    def exit_state(self):
        # input handler into command change state
        pass

    def enter_state(self):
        # input handler into command change state
        pass
