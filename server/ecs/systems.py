import pygame


def draw_system(surface, graphics):
    for graphic_component in graphics:
        if graphic_component.is_circle:
            pygame.draw.circle(surface, (255, 255, 255), graphic_component.rect.center, graphic_component.radius)
        else:
            surface.blit(graphic_component.surface, graphic_component.rect)


def old_move_system(entity, off_bounds_handler, x_dir=0, y_dir=0):
    velocity_component = entity.components["velocity"]
    graphic_component = entity.components["graphics"]
    new_x = velocity_component.x_velocity * x_dir
    new_y = velocity_component.y_velocity * y_dir
    graphic_component.rect.move_ip(new_x, new_y)
    off_bounds_handler(entity)


def move_system(entity, off_bounds_handler, x_dir=0, y_dir=0):
    x_vel, y_vel = entity.get_vel()
    updated_x = x_vel * x_dir
    updated_y = y_vel * y_dir
    entity.shape.move_ip(updated_x, updated_y)
    off_bounds_handler(entity)


def collision_detection_system(c_object, entities):
    for entity in entities:
        if c_object.shape == entity.shape:
            continue
        elif pygame.Rect.colliderect(c_object.shape, entity.shape):
            return True
    return False
