from ecs.entities import Player, Ball, State_Text

class Pong():
    def __init__(self, match_state):
        self.match_state = match_state
        self.player1, self.player2 = "", ""

    def update(self):
        if self.match_state == "wait":
            # Wait for both players to join match and press start
            pass
        elif self.match_state == "start":
            # Start playing game
            pass
        elif self.match_state == "end":
            # Set the winner and wait for rematch/quit response
            pass

    def set_players(self, players: (str, str)):
        self.player1, self.player2 = players

    def process_input(self, player_id: int, player_input: str):
        if self.player1 == player_id:
            pass
        else:
            pass
