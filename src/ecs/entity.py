class Entity():
    def __init__(self, name):
        self.name = name
        self.components = dict()

    def set_components(self):
        pass

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name
