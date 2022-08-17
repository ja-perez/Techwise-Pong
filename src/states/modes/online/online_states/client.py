import pygame
import pygwidgets
from states.state import State
from Constants import *
from states.modes.online.online_states.online_commands import MatchCommand, up_command, down_command, ready_up, \
    leave_command
from commands.command import ActiveOn
from ecs.entities import Player, Ball, State_Text, Score
from ecs.entity_manager import EntityManager
from ecs.systems import draw_system


class OnlineMatch(State):
    def __init__(self, online, join_private=False):
        State.__init__(self, online.game)
        self.online = online
        self.match_id = 0
        self.join_private = join_private
        self.network, self.server_reply = self.online.network, ""
        self.curr_match, self.match_state = None, "connecting"
        self.data, self.curr_player = "ping", 0
        self.register_commands()
        # Original method for creating objects
        self.create_objects()

    def update(self):
        if not self.match_id:
            for event in pygame.event.get():
                if self.join_private:
                    # If code is submitted then send to server and request to join match
                    # If user wants to create private match then send match id to server
                    if self.code_input.handleEvent(event):
                        friend_code = self.code_input.getValue()
                        self.server_reply = self.network.send("join_private " + friend_code)
                    # Check if create private match button is pressed
                    if self.private_match_btn.handleEvent(event):
                        self.server_reply = self.network.send("create_private")
                else:
                    self.server_reply = self.network.send("join_public")
                    # Send request to server to join a match
                    # Update match state depending on answer
                    # If no matches then ask to try again or return to lobby
                    # If match found then set match id to server response
                    pass
                # If server reply is a dict then we have been assigned a match
                if type(self.server_reply) == dict:
                    self.curr_match = self.server_reply
                    self.match_id = self.server_reply["match_id"]
                    print(self.server_reply)
                else:
                    # Server could not find match, or no matches are available
                    # Print error and ask player to try again or go back to lobby
                    pass
                # Check if player pressed ESC to return to lobby
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.online.online_state = self.online.states["lobby"]
        else:
            # Currently in a match - Need to check match state
            self.match_state = self.curr_match["match_state"]
            if self.match_state == "end":
                for event in pygame.event.get():
                    # Check return to lobby button is pressed
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.network.send("leave")
                        self.online.online_state = self.online.states["lobby"]
            else:
                command_queue = self.ih.handle_input()
                for command, args in command_queue:
                    command.execute(args[0])
                reply = self.network.send(self.data)
                if reply == "goodbye":
                    self.online.online_state = self.online.states["lobby"]
                if "match_id" in reply:
                    self.curr_match = self.network.send(self.data)

    def render(self):
        if not self.match_id:
            draw_system(self.game.screen, self.g_manager.all_entity_types("Player", "Score"))
            if self.join_private:
                # Print prompt for entering friend code or to create private match
                self.code_prompt.draw()
                self.code_input.draw()
                self.private_match_btn.draw()
            else:
                # Print "looking for open matches"
                self.public_prompt.draw()
                pass
            self.leave_prompt.draw()
        else:  # In match
            # Need to check match state
            # If waiting, then prompt to press start or if waiting for other player
            # If start then display the updated position of all objects
            # If game over then display player outcome and option to rematch or return to lobby
            self.match_state = self.curr_match["match_state"]
            self.curr_player = self.curr_match["curr_player"]
            if self.match_state == "waiting":
                if self.curr_match[self.curr_player][2] == "waiting":
                    # Print Waiting on self to ready up
                    self.ready_up_prompt.draw()
                    pass
                else:
                    # Print Waiting on other player to ready up
                    self.waiting_prompt.draw()
                    pass
                self.update_objects()
                draw_system(self.game.screen, self.g_manager.all_entity_types("Player", "Score"))
            elif self.match_state == "start":
                self.update_objects()
                draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))
            elif self.match_state == "end":
                # display player game outcome
                # wait for client to choose to leave or rematch
                self.start_positions()
                self.update_objects()
                if self.curr_match["winner"] == str(self.curr_player):
                    self.first_prompt.draw()
                else:
                    self.last_prompt.draw()
                draw_system(self.game.screen, self.g_manager.all_entity_types("Player", "Score"))
            if self.match_state != "start":
                self.leave_prompt.draw()

    def register_commands(self):
        self.move_up = MatchCommand(ActiveOn.BOTH, up_command, self)
        self.move_down = MatchCommand(ActiveOn.BOTH, down_command, self)
        self.set_ready = MatchCommand(ActiveOn.BOTH, ready_up, self)
        self.player_leave = MatchCommand(ActiveOn.PRESSED, leave_command, self)
        self.ih.register_command(pygame.K_w, self.move_up)
        self.ih.register_command(pygame.K_s, self.move_down)
        self.ih.register_command(pygame.K_SPACE, self.set_ready)
        self.ih.register_command(pygame.K_ESCAPE, self.player_leave)

    def create_objects(self):
        self.g_manager = EntityManager()
        self.create_players()
        self.create_balls()
        self.create_scores()
        self.create_prompts()

    def create_players(self):
        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")

        p1_cords = BALL_RADIUS * 2, GAME_H - self.player_2.get_size()[1] / 2
        p2_cords = GAME_W * 2 - self.player_2.get_size()[0] - BALL_RADIUS * 2, \
                   GAME_H - self.player_2.get_size()[1] / 2
        self.player_1.set_cords(p1_cords[0], p1_cords[1])
        self.player_2.set_cords(p2_cords[0], p2_cords[1])

        self.g_manager.register_entity(self.player_1)
        self.g_manager.register_entity(self.player_2)

    def create_balls(self):
        self.ball_0 = Ball("ball 0")
        self.g_manager.register_entity(self.ball_0)
        ball_0_cords = GAME_W - BALL_RADIUS, GAME_H - BALL_RADIUS
        self.ball_0.set_cords(ball_0_cords[0], ball_0_cords[1])

    def create_scores(self):
        self.score_1 = Score("Player 1: ", SCORE_SIZE, WHITE, FONT_NAME)
        self.score_2 = Score("Player 2: ", SCORE_SIZE, WHITE, FONT_NAME)
        self.score_1.set_pos(self.player_1.surface.get_width() * 2, 0)
        self.score_2.set_pos(GAME_W * 2 - self.score_2.surface.get_width() * 2, 0)
        self.g_manager.register_entity(self.score_1)
        self.g_manager.register_entity(self.score_2)

    def create_prompts(self):
        # Private Match Prompts and buttons
        prompt = "Enter a 4 digit friend code or\ncreate a private match and have someone\n" \
                 "enter your code."
        self.code_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                  fontSize=SCORE_SIZE, textColor=WHITE,
                                                  fontName=FONT_NAME, justified="center")
        code_prompt_rect = self.code_prompt.getRect().width, self.code_prompt.getRect().height
        self.code_prompt.moveXY(GAME_W - code_prompt_rect[0] / 2, GAME_H / 2)

        text_input = 200
        self.private_match_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Create Private Match',
                                                       fontName=FONT_NAME, width=text_input)
        btn_rect = self.private_match_btn.getRect().width, self.private_match_btn.getRect().height
        self.private_match_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H)

        input_rect = GAME_W - text_input / 2, GAME_H + 50
        self.code_input = pygwidgets.InputText(self.game.screen, input_rect, initialFocus=False,
                                               textColor=RED, fontName=FONT_NAME, fontSize=MENU_FONT_SIZE)

        # Public Match Prompts
        prompt = "Waiting for open match..."
        self.public_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                    fontSize=TEXT_SIZE, textColor=WHITE,
                                                    fontName=FONT_NAME, justified="center")
        public_prompt_rect = self.public_prompt.getRect().width, self.public_prompt.getRect().height
        self.public_prompt.moveXY(GAME_W - public_prompt_rect[0] / 2, GAME_H - public_prompt_rect[1])

        # Waiting Prompts
        prompt = "Press Space to Ready Up"
        self.ready_up_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                      fontSize=TEXT_SIZE, textColor=WHITE,
                                                      fontName=FONT_NAME, justified="center")
        ready_up_prompt_rect = self.ready_up_prompt.getRect().width, self.ready_up_prompt.getRect().height
        self.ready_up_prompt.moveXY(GAME_W - ready_up_prompt_rect[0] / 2, GAME_H - ready_up_prompt_rect[1])

        prompt = "Waiting for other player"
        self.waiting_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                     fontSize=TEXT_SIZE, textColor=WHITE,
                                                     fontName=FONT_NAME, justified="center")
        waiting_prompt_rect = self.waiting_prompt.getRect().width, self.waiting_prompt.getRect().height
        self.waiting_prompt.moveXY(GAME_W - waiting_prompt_rect[0] / 2, GAME_H - waiting_prompt_rect[1])

        # Leave Match Prompt
        prompt = "Press Escape to return to Lobby"
        self.leave_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                   fontSize=MENU_FONT_SIZE, textColor=WHITE,
                                                   fontName=FONT_NAME, justified="center")
        leave_prompt_rect = self.leave_prompt.getRect().width, self.leave_prompt.getRect().height
        self.leave_prompt.moveXY(0, WIN_H - leave_prompt_rect[1])

        # End Game Prompt
        prompt = "Congratulations, You're the Winner!"
        self.first_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                   fontSize=TEXT_SIZE, textColor=WHITE,
                                                   fontName=FONT_NAME, justified="center")
        first_prompt_rect = self.first_prompt.getRect().width, self.first_prompt.getRect().height
        self.first_prompt.moveXY(GAME_W - first_prompt_rect[0] / 2, GAME_H - first_prompt_rect[1])

        prompt = "Better Luck Next Time, Chump"
        self.last_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                  fontSize=TEXT_SIZE, textColor=WHITE,
                                                  fontName=FONT_NAME, justified="center")
        last_prompt_rect = self.last_prompt.getRect().width, self.last_prompt.getRect().height
        self.last_prompt.moveXY(GAME_W - last_prompt_rect[0] / 2, GAME_H - last_prompt_rect[1])

    def update_objects(self):
        # Updating Moving Objects
        p1_x, p1_y = self.curr_match[1][0]
        p2_x, p2_y = self.curr_match[2][0]
        ball_x, ball_y = self.curr_match['ball']
        self.player_1.set_cords(p1_x, p1_y)
        self.player_2.set_cords(p2_x, p2_y)
        self.ball_0.set_cords(ball_x, ball_y)

        # Updating Scores
        if self.curr_match["match_state"] == "waiting":
            self.score_1.name = "Player 1: " + self.curr_match[1][2]
            self.score_2.name = "Player 2: " + self.curr_match[2][2]
        else:
            self.score_1.name = "Player 1: " + str(self.curr_match[1][1])
            self.score_2.name = "Player 2: " + str(self.curr_match[2][1])
        self.score_1.update_graphics()
        self.score_2.update_graphics()
        self.g_manager.update_entity_component(self.score_1, "graphics")
        self.g_manager.update_entity_component(self.score_2, "graphics")
        self.g_manager.update_entity_component(self.score_1, "text")
        self.g_manager.update_entity_component(self.score_2, "text")

    def start_positions(self):
        p1_x, p1_y = BALL_RADIUS * 2, GAME_H - self.player_1.get_size()[1] / 2
        p2_x, p2_y = GAME_W * 2 - self.player_2.get_size()[0] - BALL_RADIUS * 2, \
                     GAME_H - self.player_2.get_size()[1] / 2
        self.player_1.set_cords(p1_x, p1_y)
        self.player_2.set_cords(p2_x, p2_y)

        ball_0_cords = GAME_W - BALL_RADIUS, GAME_H - BALL_RADIUS
        self.ball_0.set_cords(ball_0_cords[0], ball_0_cords[1])

    def enter_state(self):
        # If private - print prompt for entering friend code
        # If public - print prompt "Waiting for open matches"
        # Print paddles and scores in starting position
        self.render()
        pass

    def exit_state(self):
        pass

    def reset(self):
        pass
