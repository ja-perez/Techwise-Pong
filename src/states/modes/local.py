import pygame
from states.state import State
from Constants import *
from ecs.entities import Player, Ball, Score
from ecs.entity_manager import EntityManager
from states.modes.localcommands import *
from ecs.systems import *


class Local(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.player_c = LocalCommand(ActiveOn.PRESSED, player_commands, self)
        self.register_commands()
        self.create_players()
        self.create_balls()
        self.create_scoreboards()
        self.objects = list()

    def update(self):

        command_queue = self.ih.handle_input()
        for command, args in command_queue:
            command.execute(args[0])

    def render(self):
        draw_system(self.game.screen, self.players.all_component_instances("graphics"), self.objects)
        draw_system(self.game.screen, self.balls.all_component_instances("graphics"), self.objects)
        draw_system(self.game.screen, self.scores.all_component_instances("graphics"), self.objects)

    def register_commands(self):
        # Player 1 movement
        self.ih.register_command(pygame.K_LEFT, self.player_c)
        self.ih.register_command(pygame.K_RIGHT, self.player_c)
        self.ih.register_command(pygame.K_UP, self.player_c)
        self.ih.register_command(pygame.K_DOWN, self.player_c)
        # Player 2 movement
        self.ih.register_command(pygame.K_a, self.player_c)
        self.ih.register_command(pygame.K_d, self.player_c)
        self.ih.register_command(pygame.K_w, self.player_c)
        self.ih.register_command(pygame.K_s, self.player_c)

    def create_players(self):
        # create player 1:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        self.player1 = Player("player 1")
        self.player1.set_pos(BALL[0], GAME_H - PADDLE[1] / 2)
        self.player1.set_vel(0, 10)
        # create player 2:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        self.player2 = Player("player 2")
        self.player2.set_pos(GAME_W * 2 - PADDLE[0] - BALL[0], GAME_H - PADDLE[1] / 2)
        self.player2.set_vel(0, 10)
        # register both players with a player entity manager
        self.players = EntityManager()
        self.players.register_entity(self.player1)
        self.players.register_entity(self.player2)

    def create_balls(self):
        # create ball and set position to the center of the screen
        self.ball = Ball("ball")
        self.ball.set_pos(GAME_W, GAME_H - BALL[1] / 2)
        # register ball with a ball entity manager
        self.balls = EntityManager()
        self.balls.register_entity(self.ball)

    def create_scoreboards(self):
        self.score1 = Score(self.player1.get_name() + " score: " + self.player1.get_score(),
                            SCORE_SIZE, WHITE)
        self.score1.set_pos(self.player1.surface.get_width() * 1.5, 0)
        self.score2 = Score(self.player2.get_name() + " score: " + self.player2.get_score(),
                            SCORE_SIZE, WHITE)
        self.score2.set_pos(GAME_W * 2 - self.score2.surface.get_width() * 1.5, 0)
        # register scores with a score entity manager
        self.scores = EntityManager()
        self.scores.register_entity(self.score1)
        self.scores.register_entity(self.score2)

    def exit_state(self):
        self.game.running = False

    def pause_command(self):
        self.change_state("mainmenu")
