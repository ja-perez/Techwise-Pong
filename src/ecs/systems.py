def draw_system(surface, graphics, objects):
    for graphic_component in graphics:
        objects.append(surface.blit(graphic_component.surface, graphic_component.rect))
