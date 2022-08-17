import pygame
import pygwidgets
from states.state import State
from Constants import *
from states.modes.online.online_states.online_commands import MatchCommand, up_command, down_command, ready_up
from commands.command import ActiveOn
from ecs.entities import Player, Ball, State_Text, Score
from ecs.entity_manager import EntityManager
from ecs.systems import draw_system


class Online_Match(State):
    def __init__(self, game, online, is_private=False):
        State.__init__(self, game)
        self.online, self.is_private = online, is_private
        self.network = self.online.network
        self.game_state, self.curr_match = None, None
        self.data, self.curr_player = "", 0
        self.register_commands()
        self.create_objects()

    def update(self, state):
        if self.curr_match["match_state"] != "end":
            command_queue = self.ih.handle_input()
            for command, args in command_queue:
                command.execute(args[0])
        else:
            for event in pygame.event.get():
                if self.exit_button.handleEvent(event):
                    print("returning to lobby")
                    self.exit_state()
                    state.curr_state = state.states["self"]
        if self.data:
            self.curr_match = self.network.send(self.data)
            if self.data == "ready":
                self.data = "ping"
            print(self.curr_match, type(self.curr_match))
        if self.curr_match["match_state"] == "wait":
            pass
        elif self.curr_match["match_state"] == "start":
            if 'match_id' in self.curr_match:
                print("Player 1:", self.curr_match[1][0])
                print("Player 2:", self.curr_match[2][0])
                p1_x, p1_y = self.curr_match[1][0]
                p2_x, p2_y = self.curr_match[2][0]
                ball_x, ball_y = self.curr_match["ball"]
                self.player_1.set_cords(p1_x, p1_y)
                self.player_2.set_cords(p2_x, p2_y)
                self.ball_0.set_cords(ball_x, ball_y)
        elif self.curr_match["match_state"] == "end":
            pass
            # TODO: Create texts for displaying if client is winner or loser
            # TODO: Also need to implement buttons for rematching or returning to server

    def render(self):
        if self.curr_match["match_state"] != "end":
            draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))
            if self.curr_match["match_state"] == "wait":
                self.update_scores()
                if self.curr_match[self.curr_player][-1] == "wait":
                    self.game.screen.blit(self.start_msg.components["graphics"].surface,
                                          self.start_msg.components["graphics"].rect)
                else:
                    self.game.screen.blit(self.wait_msg.components["graphics"].surface,
                                          self.wait_msg.components["graphics"].rect)
            elif self.curr_match["match_state"] == "start":
                self.update_scores(1)
        else:
            if self.curr_match["winner"] == str(self.curr_match["curr_player"]):
                self.game.screen.blit(self.winning_text.components["graphics"].surface,
                                      self.winning_text.components["graphics"].rect)
            else:
                self.game.screen.blit(self.loser_text.components["graphics"].surface,
                                      self.loser_text.components["graphics"].rect)
            self.exit_button.draw()

    def register_commands(self):
        self.press_up = MatchCommand(ActiveOn.BOTH, up_command, self)
        self.press_down = MatchCommand(ActiveOn.BOTH, down_command, self)
        self.press_space = MatchCommand(ActiveOn.BOTH, ready_up, self)
        self.ih.register_command(pygame.K_w, self.press_up)
        self.ih.register_command(pygame.K_s, self.press_down)
        self.ih.register_command(pygame.K_SPACE, self.press_space)

    def create_objects(self):
        self.g_manager = EntityManager()
        self.create_players()
        self.create_balls()
        self.create_buttons()
        self.create_texts()
        self.set_text_positions()

    def create_players(self):
        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")
        self.g_manager.register_entity(self.player_1)
        self.g_manager.register_entity(self.player_2)

    def create_balls(self):
        self.ball_0 = Ball("ball 0")
        self.g_manager.register_entity(self.ball_0)

    def create_buttons(self):
        self.exit_button = pygwidgets.TextButton(self.game.screen, (0, 0),
                                                 "Back to Lobby")
        self.exit_button.moveXY(GAME_W - self.exit_button.getRect().width / 2,
                                GAME_H - self.exit_button.getRect().height / 2)

    def create_texts(self):
        self.start_msg = State_Text("Press Space to Ready Up!", TEXT_SIZE, WHITE)
        self.wait_msg = State_Text("Waiting for Other Player", TEXT_SIZE, WHITE)
        self.winning_text = State_Text("Congratulations, You're the Winner", TEXT_SIZE, WHITE)
        self.loser_text = State_Text("Better Luck Next Time", TEXT_SIZE, WHITE)
        self.score_1 = Score("Player 1: ", SCORE_SIZE, WHITE)
        self.score_2 = Score("Player 2: ", SCORE_SIZE, WHITE)
        self.g_manager.register_entity(self.score_1)
        self.g_manager.register_entity(self.score_2)

    def set_text_positions(self):
        self.start_msg.set_pos(GAME_W - self.start_msg.components["graphics"].rect.width / 2,
                               self.start_msg.components["graphics"].rect.height * 2)
        self.wait_msg.set_pos(GAME_W - self.wait_msg.components["graphics"].rect.width / 2,
                              self.wait_msg.components["graphics"].rect.height * 2)
        self.winning_text.set_pos(GAME_W - self.winning_text.components["graphics"].rect.width / 2,
                                  self.winning_text.components["graphics"].rect.height * 2)
        self.loser_text.set_pos(GAME_W - self.loser_text.components["graphics"].rect.width / 2,
                                self.loser_text.components["graphics"].rect.height * 2)
        self.score_1.set_pos(self.player_1.surface.get_width() * 2, 0)
        self.score_2.set_pos(GAME_W * 2 - self.score_2.surface.get_width() * 2, 0)

    def set_match(self, match_id):
        self.curr_match = match_id

    def update_scores(self, toggle=0):
        if not toggle:
            self.score_1.name = "Player 1: " + self.curr_match[1][-1]
            self.score_2.name = "Player 2: " + self.curr_match[2][-1]
        else:
            self.score_1.name = "Player 1: " + str(self.curr_match[1][1])
            self.score_2.name = "Player 2: " + str(self.curr_match[2][1])
        self.score_1.update_graphics()
        self.score_2.update_graphics()

    def enter_state(self):
        if not self.is_private:
            reply = self.online.network.send("join_public")
            if "match_id" in reply:
                self.curr_match = reply
                p1_x, p1_y = reply[1][0]
                p2_x, p2_y = reply[2][0]
                ball_x, ball_y = reply["ball"]
                self.player_1.set_cords(p1_x, p1_y)
                self.player_2.set_cords(p2_x, p2_y)
                self.ball_0.set_cords(ball_x, ball_y)
                self.curr_player = reply["curr_player"]

    def exit_state(self):
        self.server_response = None
        self.data, self.start = "", False

    def change_state(self, next_state: str):
        self.exit_state()
        self.online.change_state(next_state)
        self.online.curr_state.enter_state()