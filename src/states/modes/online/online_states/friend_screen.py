import pygame, pygwidgets
from states.state import State
from ecs.entities import State_Text
from Constants import *


class Friend_Screen(State):
    def __init__(self, game, online):
        State.__init__(self, game)
        self.online = online
        self.friend_code = online.friend_code
        self.create_objects()

    def update(self, state):
        for event in pygame.event.get():
            if self.private_match_btn.handleEvent(event):
                match_id = self.online.network.send("create_private")
                print(match_id)
            if self.back_to_lobby_btn.handleEvent(event):
                state.curr_state = state.states["self"]
            if self.code_input.handleEvent(event):
                f_code = self.code_input.getValue()
                match_id = self.online.network.send("join_private " + f_code)

    def render(self):
        graphic_component = self.client_code.components["graphics"]
        self.game.screen.blit(graphic_component.surface, graphic_component.rect)
        self.code_prompt.draw()
        self.code_input.draw()
        self.private_match_btn.draw()
        self.back_to_lobby_btn.draw()

    def create_objects(self):
        friend_code_text = "Your friend code is: " + self.friend_code
        self.client_code = State_Text(friend_code_text, SCORE_SIZE, WHITE)
        graphic_component = self.client_code.components["graphics"]
        self.client_code.set_pos(GAME_W - graphic_component.rect.width / 2,
                                 GAME_H / 2 - graphic_component.rect.height)

        # text input handler - width default 200
        prompt = "Enter a 4 digit friend code\nor have someone else enter your code."
        self.code_prompt = pygwidgets.DisplayText(self.game.screen, (0, 0), value=prompt,
                                               fontSize=SCORE_SIZE, textColor=WHITE,
                                               justified="center")
        code_prompt_rect = self.code_prompt.getRect().width, self.code_prompt.getRect().height
        self.code_prompt.moveXY(GAME_W - code_prompt_rect[0] / 2, GAME_H / 2 + code_prompt_rect[1])

        text_input = 200
        input_rect = GAME_W - text_input / 2, GAME_H
        self.code_input = pygwidgets.InputText(self.game.screen, input_rect, initialFocus=False,
                                               textColor=RED, fontSize=SCORE_SIZE)

        # create private match button
        self.private_match_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Create Private Match')
        btn_rect = self.private_match_btn.getRect().width, self.private_match_btn.getRect().height
        self.private_match_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H + btn_rect[1])

        # return to lobby button
        self.back_to_lobby_btn = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return to Lobby')
        btn_rect = self.back_to_lobby_btn.getRect().width, self.back_to_lobby_btn.getRect().height
        self.back_to_lobby_btn.moveXY(GAME_W - btn_rect[0] / 2, GAME_H + btn_rect[1] * 2)