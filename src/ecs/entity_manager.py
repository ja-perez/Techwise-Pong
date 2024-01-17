class EntityManager():
    def __init__(self):
        self.component_to_entity = dict()
        self.entity_types = dict()

    def register_entity(self, entity):
        for component_type in entity.components:
            if component_type not in self.component_to_entity:
                self.component_to_entity[component_type] = list()
            self.component_to_entity[component_type].append(entity)
        if entity.e_type not in self.entity_types:
            self.entity_types[entity.e_type] = list()
        self.entity_types[entity.e_type].append(entity)

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

    def all_entity_types(self, *get_type):
        for e_type in self.entity_types:
            if e_type in get_type:
                for entity in self.entity_types[e_type]:
                    yield entity.components["graphics"]

    def update_entity_component(self, entity, component_type):
        for i, old_entity in enumerate(self.component_to_entity[component_type]):
            if old_entity == entity:
                self.component_to_entity[component_type][i] = entity
