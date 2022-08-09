from ecs.entities import Player
from ecs.systems import move_system
# temp
from ecs.Constants import *


# TODO: Create player objects, ball objects, and implement respective game mechanics
# TODO: Properly update client for a finished match - Send a closed message?
class Pong():
    def __init__(self, match_state):
        self.match_state = match_state
        self.player_1, self.player_2 = Player("Player 1"), Player("Player 2")

    def update(self):
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
        # temp - verifying input handler is working
        p1_move_text = self.player_1.get_name() + " vel: " + str(self.player_1.get_y_vel())
        p2_move_text = self.player_2.get_name() + " vel: " + str(self.player_2.get_y_vel())
        player_moves = p1_move_text + '\n' + p2_move_text
        # temp - verifying player object works with movement
        move_system(self.player_1, self.off_bounds_handler, 0, self.player_1.y_dir)
        move_system(self.player_2, self.off_bounds_handler, 0, self.player_2.y_dir)
        p1_size = self.player_1.get_name() + " pos: " + str(self.player_1.get_pos())
        p2_size = self.player_2.get_name() + " pos: " + str(self.player_2.get_pos())
        p_sizes = p1_size + '\n' + p2_size
        return p_sizes

    def set_players(self, players: (str, str)):
        self.player_1.client_id, self.player_2.client_id = players

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

    def off_bounds_handler(self, entity):
        entity.shape.top = max(entity.shape.top, 0)
        entity.shape.bottom = min(entity.shape.bottom, WIN_H)
