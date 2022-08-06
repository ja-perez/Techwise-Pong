from ecs.entity import Entity
from ecs.components import VelocityComponent
from Constants import *
import pygame


class Player(Entity):
    def __init__(self, name="", client_id=""):
        Entity.__init__(self, name)
        self.client_id = client_id
        self.score = 0
        self.curr_state = "wait"
        self.set_components("velocity", VelocityComponent(0, 5))
        # temp
        self.move = ""

    def set_vel(self, x=0, y=0):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def set_dir(self, move: str):
        if (self.get_y_vel() > 0 and move == "down") or (self.get_y_vel() < 0 and move == "up"):
            y_comp = self.get_y_vel()
            y_comp *= -1
            self.set_vel(0, y_comp)

    def set_id(self, new_id: str):
        self.client_id = new_id

    def set_score(self, increment):
        self.score += increment

    def set_state(self, new_state: str):
        self.curr_state = new_state

    def get_y_vel(self):
        return self.components["velocity"].y_velocity

    def get_id(self):
        return self.client_id

    def get_score(self) -> int:
        return self.score

    def get_state(self):
        return self.curr_state


class Ball(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.surface = pygame.Surface(BALL)
        self.surface.fill(WHITE)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)
        self.components["graphics"].is_circle = True
        self.components["graphics"].radius = BALL_RADIUS
        self.components["velocity"] = VelocityComponent(0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def x_vel(self):
        return self.components["velocity"].x_velocity

    def y_vel(self):
        return self.components["velocity"].y_velocity


class Score(Entity):
    def __init__(self, title, size, color):
        Entity.__init__(self, title)
        self.color = color
        self.size = size
        self.components["text"] = TextComponent(title, size, color)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)

    def update_surface(self):
        self.surface = self.components["text"].font.render(self.name, False, self.color)

    def update_graphics(self):
        self.update_surface()
        self.components["graphics"].surface = self.surface


class State_Text(Entity):
    def __init__(self, title, size, color):
        Entity.__init__(self, title)
        self.components["text"] = TextComponent(title, size, color)
        self.surface = self.components["text"].font.render(title, False, color)
        self.components["graphics"] = GraphicComponent(self.surface, 0, 0)

    def set_pos(self, x, y):
        self.components["graphics"].rect.move_ip(x, y)
