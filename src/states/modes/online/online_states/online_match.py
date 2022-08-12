import pygame, pickle
from states.state import State
from Constants import *
from states.modes.online.online_states.online_commands import MatchCommand, up_command, down_command, ready_up
from commands.command import ActiveOn
from ecs.entities import Player
from ecs.entity_manager import EntityManager
from ecs.systems import draw_system

class Online_Match(State):
    def __init__(self, game, online, is_private=False):
        State.__init__(self, game)
        self.online, self.is_private = online, is_private
        self.network = self.online.network
        self.game_state = None

        self.curr_match, self.server_response = None, None
        self.data, self.start = "", False
        self.register_commands()
        self.create_objects()

    def update(self, state):
        command_queue = self.ih.handle_input()
        for command, args in command_queue:
            command.execute(args[0])

        if self.data:
            self.server_response = self.network.send(self.data)
            print(self.server_response, type(self.server_response))
            if 'moves' in self.server_response:
                moves = self.server_response.split()[1:]
                print("Player 1:", moves[0:2])
                print("Player 2:", moves[2:])
                self.player_1.set_cords(int(moves[0]), int(moves[1]))
                self.player_2.set_cords(int(moves[2]), int(moves[3]))
            else:
                print("Player 1:", self.server_response["player 1"][0])
                print("Player 2:", self.server_response["player 2"][0])
                p1_x, p1_y = self.server_response["player 1"][0]
                p2_x, p2_y = self.server_response["player 2"][0]
                self.player_1.set_cords(p1_x, p1_y)
                self.player_2.set_cords(p2_x, p2_y)

    def render(self):
        draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))

    def register_commands(self):
        self.press_up = MatchCommand(ActiveOn.BOTH, up_command, self)
        self.press_down = MatchCommand(ActiveOn.BOTH, down_command, self)
        self.press_space = MatchCommand(ActiveOn.PRESSED, ready_up, self)
        self.ih.register_command(pygame.K_w, self.press_up)
        self.ih.register_command(pygame.K_s, self.press_down)
        self.ih.register_command(pygame.K_SPACE, self.press_space)

    def create_objects(self):
        self.g_manager = EntityManager()
        self.create_players()

    def create_players(self):
        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")
        self.g_manager.register_entity(self.player_1)
        self.g_manager.register_entity(self.player_2)

    def set_match(self, match_id):
        self.curr_match = match_id

    def enter_state(self):
        if not self.is_private:
            reply = self.online.network.send("join_public")
            if "match_id" in reply:
                self.curr_match = reply.split()[1]

    def exit_state(self):
        self.curr_match, self.server_response = None, None
        self.data, self.start = "", False
