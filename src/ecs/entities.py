from entity import Entity


class Player(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.score = 0


class Ball(Entity):
    def __init(self, name):
        Entity.__init__(self, name)
