def draw_system(surface, graphics, objects):
    for graphic_component in graphics:
        objects.append(surface.blit(graphic_component.surface, graphic_component.rect))


def move_system(entity, off_bounds_handler, x_dir, y_dir):
        velocity_component = entity.components["velocity"]
        graphic_component = entity.components["graphic"]
        new_x = velocity_component.x_velocity * x_dir
        new_y = velocity_component.y_velocity * y_dir
        graphic_component.set_pos
