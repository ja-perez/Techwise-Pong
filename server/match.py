import random
from online_pong import Pong


class Match:
    def __init__(self, match_id, private_match=False):
        self.match_id = match_id
        self.players = {1: "", 2: ""}
        self.match_state = "wait"
        self.private_match = private_match
        self.pong_match = Pong(self.match_state)

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
                self.match_state = "wait"

    def is_private(self):
        return self.private_match

    def get_id(self):
        return self.match_id

    def is_full(self):
        return self.players[1] and self.players[2]

    def is_empty(self):
        return self.players[1] or self.players[2]

    def owner_present(self):
        return str(self.match_id) in self.get_players()

    def get_state(self):
        return self.match_state

    def start_game(self):
        self.pong_match.set_players(self.get_players())
        self.match_state = "start"

    def update_game(self, player: int, player_input: str):
        self.pong_match.process_input(player, player_input)


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

    def get_open_match(self, player_id):
        try:
            match_id = self.open[0]
            self.matches[match_id].set_player(player_id)
            return match_id
        except IndexError as e:
            print(str(e))
            return "No matches available"

    def create_private_match(self, private_id):
        self.matches[private_id] = Match(private_id, True)
        self.matches[private_id].set_player(private_id)
        return self.matches[private_id].get_id()

    def get_private_match(self, private_id, player_id):
        try:
            private_id = int(private_id)
            self.matches[private_id].set_player(player_id)
            return self.matches[private_id].get_id()
        except KeyError as e:
            print(str(e))
            return "Match " + str(private_id) + " does not exist"

    # TODO: Change this to update match with inputs and remove match_handler: process input method
    def update_match(self, match_id, player_id):
        try:
            self.matches[match_id].remove_player(player_id)
        except ValueError as e:
            return str(e)

    def update_matches(self):
        remove_match = []
        for match_id in self.matches:
            curr_match = self.matches[match_id]
            if curr_match.is_full():
                if match_id in self.open:
                    self.open.remove(match_id)
                if curr_match.get_state() == "wait":
                    self.matches[match_id].start_game()
            elif match_id not in self.open:
                self.open.append(match_id)
            if curr_match.is_private() and not curr_match.owner_present():
                remove_match.append(match_id)
                self.open.remove(match_id)
        self.remove_matches(remove_match)

    def process_input(self, input_str: str, match_id: int, client_id: int):
        if "move" in input_str:
            client_input = input_str.split()[1]
            self.matches[match_id].update_game(client_id, client_input)
            # TODO: Return pickled updated online_match object instead of string #
            return "In match " + str(match_id) + ": Moving Player " + str(client_id) + " " + client_input
        else:
            return "No movement input"

    def remove_matches(self, match_ids):
        try:
            for match_id in match_ids:
                del self.matches[match_id]
        except ValueError as e:
            print(str(e))

    def number_of_matches(self):
        return len(self.matches)