class Entity():
    def __init__(self, name):
        self.name = name
        self.e_type = "Default"
        self.components = dict()
        self.is_circle = False

    def set_components(self, component_type, component):
        self.components.update({component_type: component})

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name
