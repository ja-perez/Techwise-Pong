from ecs.entity import Entity
from ecs.components import VelocityComponent
from ecs.Constants import *
import pygame
from pygame import Rect

class Player(Entity):
    def __init__(self, name="", client_id=""):
        Entity.__init__(self, name)
        self.client_id = client_id
        self.score, self.x_dir, self.y_dir = 0, 0, 0
        self.curr_state = "waiting"
        self.shape = Rect((0, 0), PADDLE)
        self.set_components("velocity", VelocityComponent(0, 10))

    def set_vel(self, x=0, y=0):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def set_y_dir(self, move: str):
        self.y_dir = (move == "down") - (move == "up")

    def set_id(self, new_id: str):
        self.client_id = new_id

    def set_score(self, increment):
        self.score += increment

    def set_state(self, new_state: str):
        self.curr_state = new_state

    def set_cords(self, x, y):
        self.shape.topleft = (x, y)

    def get_y_vel(self) -> int:
        return self.components["velocity"].y_velocity

    def get_x_vel(self) -> int:
        return self.components["velocity"].x_velocity

    def get_dirs(self) -> (int, int):
        return self.x_dir, self.y_dir

    def get_vel(self) -> (int, int):
        return self.get_x_vel(), self.get_y_vel()

    def get_pos(self) -> (int, int):
        return self.shape.topleft

    def get_center(self) -> (int, int):
        return self.shape.center

    def get_id(self) -> str:
        return self.client_id

    def get_score(self) -> int:
        return self.score

    def get_state(self) -> str:
        return self.curr_state

    def get_size(self) -> (int, int):
        return self.shape.size

    def reset_player(self):
        self.score = 0
        self.curr_state = "waiting"
        self.client_id = ""


class Ball(Entity):
    def __init__(self, name):
        Entity.__init__(self, name)
        self.x_dir, self.y_dir = 0, 0
        self.curr_state = "wait"
        self.shape = Rect((0, 0), BALL)
        self.set_components("velocity", VelocityComponent(2.5, 2.5))

    def set_vel(self, x, y):
        self.components["velocity"].x_velocity = x
        self.components["velocity"].y_velocity = y

    def set_x_dir(self, x_dir):
        self.x_dir = x_dir

    def set_y_dir(self, y_dir):
        self.y_dir = y_dir

    def toggle_y_dir(self):
        self.y_dir *= -1

    def toggle_x_dir(self):
        self.x_dir *= -1

    def get_dirs(self):
        return self.x_dir, self.y_dir

    def get_pos(self) -> (int, int):
        return self.shape.topleft

    def get_x_vel(self):
        return self.components["velocity"].x_velocity

    def get_y_vel(self):
        return self.components["velocity"].y_velocity

    def get_vel(self):
        return self.get_x_vel(), self.get_y_vel()


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
