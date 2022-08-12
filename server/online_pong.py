from ecs.entities import Player, Ball
from ecs.systems import move_system, collision_detection_system
from ecs.entity_manager import EntityManager
import random
# temp
from ecs.Constants import *


# TODO: Create player objects, ball objects, and implement respective game mechanics
# TODO: Properly update client for a finished match - Send a closed message?
class Pong():
    def __init__(self, match_state):
        self.match_state = match_state
        self.player_1, self.player_2 = Player("Player 1"), Player("Player 2")
        self.ball_0 = Ball("Ball 0")
        self.entities = [self.player_1, self.player_2, self.ball_0]
        self.start_pos()

    def update(self):
        move_system(self.player_1, self.paddle_off_bounds_handler, 0, self.player_1.y_dir)
        move_system(self.player_2, self.paddle_off_bounds_handler, 0, self.player_2.y_dir)
        move_system(self.ball_0, self.ball_off_bounds_handler, self.ball_0.x_dir, self.ball_0.y_dir)
        collision_present = collision_detection_system(self.ball_0, self.entities)
        self.collision_handler(collision_present)

        if self.match_state == "wait":
            # Wait for both players to join match and press start
            pass
        if self.match_state == "start":
            # Start playing game
            pass
        if self.match_state == "end":
            # Set the winner and wait for rematch/quit response
            pass

    def render(self):
        print("ball pos:", self.ball_0.get_pos())

    def process_input(self, player_id: int, player_input: str):
        player_id = str(player_id)
        if "move" in player_input:
            # self.match_state = "start", maybe call start game, move this into there?
            move = player_input.split()[1]
            if self.player_1.get_id() == player_id:
                self.player_1.set_y_dir(move)
            else:
                self.player_2.set_y_dir(move)
        else:  # Assume some kind of state change (wait -> start, end->wait, etc.)
            if player_input == "start":
                pass

    def get_player1_data(self):
        return self.player_1.get_pos(), self.player_1.get_score()

    def get_player2_data(self):
        return self.player_2.get_pos(), self.player_2.get_score()

    def get_ball_data(self):
        return self.ball_0.get_pos()

    def set_players(self, players: (str, str)):
        self.player_1.client_id, self.player_2.client_id = players

    def start_pos(self):
        self.player_1.shape.move_ip(BALL[0], GAME_H - PADDLE[1] / 2)
        self.player_2.shape.move_ip(GAME_W * 2 - PADDLE[0] - BALL[0], GAME_H - PADDLE[1] / 2)
        self.ball_0.shape.move_ip(GAME_W - BALL[0], GAME_H - BALL[1])
        self.ball_0.set_x_dir(1 if random.randint(0, 1) else -1)
        self.ball_0.set_y_dir(1 if random.randint(0, 1) else -1)

    def reset_ball_pos(self):
        self.ball_0.shape.topleft = GAME_W - BALL[0], GAME_H - BALL[1]
        self.ball_0.set_x_dir(1 if random.randint(0, 1) else -1)
        self.ball_0.set_y_dir(1 if random.randint(0, 1) else -1)

    def paddle_off_bounds_handler(self, entity: Player):
        entity.shape.top = max(entity.shape.top, 0)
        entity.shape.bottom = min(entity.shape.bottom, WIN_H)

    def ball_off_bounds_handler(self, entity: Ball):
        # TODO: Add collision identifier for audio fx in client
        if entity.shape.left <= 0:
            self.reset_ball_pos()
        elif entity.shape.right >= WIN_W:
            self.reset_ball_pos()
        if entity.shape.top <= 0 or entity.shape.bottom >= WIN_H:
            self.ball_0.toggle_y_dir()

    def collision_handler(self, collision_present):
        if collision_present:
            self.ball_0.toggle_x_dir()
