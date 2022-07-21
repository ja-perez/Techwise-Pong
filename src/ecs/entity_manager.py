class EntityManager():
    def __init__(self):
        self.component_to_entity = dict()

    def register_entity(self, entity):
        for component_type in entity.components:
            if component_type not in self.component_to_entity:
                self.component_to_entity[component_type] = entity

    def unregister_entity(self, entity):
        for component_type in self.component_to_entity:
            self.component_to_entity[component_type].remove(entity)
