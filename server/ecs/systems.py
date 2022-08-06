import pygame


def draw_system(surface, graphics):
    for graphic_component in graphics:
        if graphic_component.is_circle:
            pygame.draw.circle(surface, (255, 255, 255), graphic_component.rect.center, graphic_component.radius)
        else:
            surface.blit(graphic_component.surface, graphic_component.rect)


def move_system(entity, off_bounds_handler, x_dir=0, y_dir=0):
    velocity_component = entity.components["velocity"]
    graphic_component = entity.components["graphics"]
    new_x = velocity_component.x_velocity * x_dir
    new_y = velocity_component.y_velocity * y_dir
    graphic_component.rect.move_ip(new_x, new_y)
    off_bounds_handler(entity)


def collision_detection_system(c_object, entities):
    c_object_rect = c_object.components["graphics"].rect
    for entity in entities:
        entity_rect = entity.rect
        if c_object_rect == entity_rect:
            continue
        elif pygame.Rect.colliderect(c_object_rect, entity_rect):
            return True
    return False
