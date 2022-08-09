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


def ai_system(player_entity, ball_entity, off_bounds_handler, y_dir = 0):
    velocity_component = player_entity.components["velocity"]
    graphic_component = player_entity.components["graphics"]
    new_y = velocity_component.y_velocity * y_dir
    if player_entity.components["graphics"].rect.centery < ball_entity.components["graphics"].rect.top:
        #and player_entity.components["graphics"].rect.bottom < WIN_H:
        player_entity.components["graphics"].rect.move_ip(0, 10)
    if player_entity.components["graphics"].rect.centery > ball_entity.components["graphics"].rect.bottom:
        #and player_entity.components["graphics"].rect.top > 0:
        player_entity.components["graphics"].rect.move_ip(0, -10)
    off_bounds_handler(player_entity)

def collision_detection_system(c_object, entities):
    c_object_rect = c_object.components["graphics"].rect
    for entity in entities:
        entity_rect = entity.rect
        if c_object_rect == entity_rect:
            continue
        elif pygame.Rect.colliderect(c_object_rect, entity_rect):
            return True
    return False
