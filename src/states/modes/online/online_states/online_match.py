import pygame
from states.state import State
from Constants import *
from states.modes.online.online_states.online_match_commands import MatchCommand, up_command, down_command
from commands.command import ActiveOn


class Online_Match(State):
    def __init__(self, game, online, is_private=False):
        State.__init__(self, game)
        self.register_commands()
        self.online = online
        self.network = self.online.network
        self.curr_match = None
        self.is_private = is_private
        self.server_response = None

    def update(self, state):
        command_queue = self.ih.handle_input()
        for command, args in command_queue:
            command.execute(args[0])

    def render(self):
        print(self.server_response)

    def register_commands(self):
        self.press_up = MatchCommand(ActiveOn.PRESSED, up_command, self)
        self.press_down = MatchCommand(ActiveOn.PRESSED, down_command, self)
        self.ih.register_command(pygame.K_w, self.press_up)
        self.ih.register_command(pygame.K_s, self.press_down)

    def set_match(self, match_id):
        self.curr_match = match_id

    def enter_state(self):
        if not self.is_private:
            self.curr_match = self.online.network.send("join_public")

    def exit_state(self):
        pass
