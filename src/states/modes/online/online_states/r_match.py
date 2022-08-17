import pygame
import pygwidgets
from states.state import State
from Constants import *
from states.modes.online.online_states.online_commands import MatchCommand, up_command, down_command, ready_up
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
                if type(self.server_reply) == dict:
                    self.curr_match = self.server_reply
                    self.match_id = self.server_reply["match_id"]
                    print(self.server_reply)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.online.online_state = self.online.states["lobby"]
        else:
            # Currently in a match
            # Need to check match state
            # If still waiting then only read start input
            # If playing then read movement input
            # If game over then read option input
            pass

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
        else:   # In match
            # Need to check match state
            # If waiting, then prompt to press start or if waiting for other player
            # If start then display the updated position of all objects
            # If game over then display player outcome and option to rematch or return to lobby
            draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))
        self.leave_prompt.draw()

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

        # Leave Match Prompt
        prompt = "Press Escape to return to Lobby"
        self.leave_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                                    fontSize=MENU_FONT_SIZE, textColor=WHITE,
                                                    fontName=FONT_NAME, justified="center")
        leave_prompt_rect = self.leave_prompt.getRect().width, self.leave_prompt.getRect().height
        self.leave_prompt.moveXY(0, WIN_H - leave_prompt_rect[1])

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
