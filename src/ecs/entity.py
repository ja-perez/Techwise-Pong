from components import *


class Entity():
    def __init__(self, name):
        self.name = name
        self.components = dict()

    def set_components(self, component_type, component):
        self.components[component_type] = component
