class EntityManager():
    def __init__(self):
        self.component_to_entity = dict()

    def register_entity(self, entity):
        for component_type in entity.components:
            if component_type not in self.component_to_entity:
                self.component_to_entity[component_type] = list()
            self.component_to_entity[component_type].append(entity)

    def unregister_entity(self, entity):
        for component_type in self.component_to_entity:
            if entity in self.component_to_entity[component_type]:
                self.component_to_entity[component_type].remove(entity)

    def all_component_instances(self, component_type):
        for entity in self.component_to_entity[component_type]:
            yield entity.components[component_type]

    def all_active_component_instances(self, component_type):
        for entity in self.component_to_entity["velocity"]:
            if entity in self.component_to_entity[component_type]:
                yield entity.components[component_type]