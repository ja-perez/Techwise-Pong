def draw_system(surface, graphics, objects):
    for graphic_component in graphics:
        objects.append(surface.blit(graphic_component.surface, graphic_component.rect))


def move_system(entity, off_bounds_handler, x_dir=0, y_dir=0):
    velocity_component = entity.components["velocity"]
    graphic_component = entity.components["graphics"]
    new_x = velocity_component.x_velocity * x_dir
    new_y = velocity_component.y_velocity * y_dir
    graphic_component.rect.move_ip(new_x, new_y)
    off_bounds_handler(entity)


def collision_detection_system():
    pass