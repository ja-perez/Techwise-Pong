class State:
    def __init__(self, game, name):
        self.game = game
        self.name = name

    def update(self):
        pass

    def state_name(self):
        return self.name

    def render(self, surface):
        pass
    
    def enter_state(self):
        # input handler into command change state
        pass

    def exit_state(self):
        # input handler into command change state
        pass

    def get_instance(self):
        return self
