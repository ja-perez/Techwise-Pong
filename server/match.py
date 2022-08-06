import random
from online_pong import Pong


class Match:
    def __init__(self, match_id, private_match=False):
        self.match_id = match_id
        self.pong_match = Pong()
        self.players = {1: "", 2: ""}
        self.match_state = "idle"
        self.private_match = private_match

    def set_player(self, player_id):
        player_id = str(player_id)
        if not self.players[1] and not self.players[2]:
            player_pos = random.randint(1, 2)
            self.players[player_pos] = player_id
        elif self.players[1]:
            self.players[2] = player_id
        else:
            self.players[1] = player_id

    def get_players(self):
        return self.players[1], self.players[2]

    def remove_player(self, player_id):
        for player in self.players:
            if self.players[player] == str(player_id):
                self.players[player] = ""
                self.match_state = "idle"

    def is_private(self):
        return self.private_match

    def get_id(self):
        return self.match_id

    def is_full(self):
        return self.players[1] and self.players[2]

    def get_state(self):
        return self.match_state


class Match_Manager:
    def __init__(self):
        self.match_ids = 10000  # Starting ID - increment by one per creation
        self.matches = {}
        self.open = []

    def print_matches(self):
        print("Match ID:", "Match State:", "Match Players", sep='\t')
        for match_id in self.matches:
            match_id = self.matches[match_id]
            print(match_id.get_id(), match_id.get_state(), match_id.get_players()
                  , sep='\t\t')

    def create_match(self):
        self.matches[self.match_ids] = Match(self.match_ids)
        self.open.append(self.match_ids)
        self.match_ids += 1

    def create_private_match(self, private_id):
        self.matches[private_id] = Match(private_id, True)
        self.matches[private_id].set_player(private_id)
        return self.matches[private_id].get_id()

    def get_open_match(self, player_id):
        try:
            match_id = self.open[0]
            self.matches[match_id].set_player(player_id)
            return match_id
        except IndexError as e:
            print(str(e))
            return "No matches available"

    def get_private_match(self, private_id, player_id):
        try:
            private_id = int(private_id)
            self.matches[private_id].set_player(player_id)
            return self.matches[private_id].get_id()
        except KeyError as e:
            print(str(e))
            return "Match " + str(private_id) + " does not exist"

    def update_match(self, match_id, player_id):
        try:
            self.matches[match_id].remove_player(player_id)
        except ValueError as e:
            return str(e)

    def update_matches(self):
        for match_id in self.matches:
            if self.matches[match_id].is_full() and match_id in self.open:
                self.open.remove(match_id)
            if not self.matches[match_id].is_full() and match_id not in self.open:
                self.open.append(match_id)

    def number_of_matches(self):
        return len(self.matches)
