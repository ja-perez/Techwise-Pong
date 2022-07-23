import pygame
import random
from states.state import State
from Constants import *
from ecs.entities import Player, Ball, Score, Pause
from ecs.entity_manager import EntityManager
from states.modes.localcommands import *
from ecs.systems import *


class Local(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.pause = True
        self.register_commands()
        self.create_players()
        self.create_balls()
        self.create_texts()
        self.set_start_positions()
        self.objects = list()
        self.scored = False

    def update(self):
        command_queue = self.ih.handle_input()
        for command, args in command_queue:
            command.execute(args[0])
        if not self.pause:
            self.p1_y_direction = self.p1_down - self.p1_up
            self.p2_y_direction = self.p2_down - self.p2_up
            move_system(self.player1, self.paddle_off_bounds_handler, 0, self.p1_y_direction)
            move_system(self.player2, self.paddle_off_bounds_handler, 0, self.p2_y_direction)
            move_system(self.ball, self.ball_off_bounds_handler)
            if self.scored:
                self.balls.unregister_entity(self.ball)
                self.create_balls()
                self.update_scores()
                self.scored = False

    def render(self):
        draw_system(self.game.screen, self.players.all_component_instances("graphics"), self.objects)
        draw_system(self.game.screen, self.balls.all_component_instances("graphics"), self.objects)
        draw_system(self.game.screen, self.scores.all_component_instances("graphics"), self.objects)
        if self.pause:
            draw_system(self.game.screen, self.texts.all_component_instances("graphics"), self.objects)

    def register_commands(self):
        # Command: press space to start
        self.start_command = LocalCommand(ActiveOn.PRESSED, toggle_pause, self)
        self.ih.register_command(pygame.K_SPACE, self.start_command)
        # Command: press up/w to move player up and down/s to move player down
        self.player_up_press = LocalCommand(ActiveOn.BOTH, up_command, self)
        self.player_down_press = LocalCommand(ActiveOn.BOTH, down_command, self)
        # Player 1 movement
        self.ih.register_command(pygame.K_w, self.player_up_press)
        self.ih.register_command(pygame.K_s, self.player_down_press)
        # Player 2 movement
        self.ih.register_command(pygame.K_UP, self.player_up_press)
        self.ih.register_command(pygame.K_DOWN, self.player_down_press)

    def create_players(self):
        # create player 1:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        # set up and down values to false and direction to 0
        self.player1 = Player("player 1")
        self.player1.set_vel(0, 10)
        self.p1_up, self.p1_down = False, False
        self.p1_y_direction = 0
        # create player 2:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        # set up and down values to false and direction to 0
        self.player2 = Player("player 2")
        self.player2.set_vel(0, 10)
        self.p2_up, self.p2_down = False, False
        self.p2_y_direction = 0
        # register both players with a player entity manager
        self.players = EntityManager()
        self.players.register_entity(self.player1)
        self.players.register_entity(self.player2)

    def set_start_positions(self):
        self.player1.set_pos(BALL[0], GAME_H - PADDLE[1] / 2)
        self.player2.set_pos(GAME_W * 2 - PADDLE[0] - BALL[0], GAME_H - PADDLE[1] / 2)
        # self.ball.set_pos(GAME_W, GAME_H - BALL[1] / 2)
        self.pause_text.set_pos(GAME_W - self.pause_text.components["graphics"].rect.width / 2, 0)
        self.score1.set_pos(self.player1.surface.get_width() * 2, 0)
        self.score2.set_pos(GAME_W * 2 - self.score2.surface.get_width() * 1.5, 0)

    def create_balls(self):
        # create ball and set position to the center of the screen
        self.ball = Ball("ball")
        random_ball_start = (random.randint(2, 5) * (1 if random.randint(0, 1) else -1))
        self.ball.set_pos(GAME_W, GAME_H - BALL[1] / 2)
        self.ball.set_vel(random_ball_start, random_ball_start)
        # register ball with a ball entity manager
        self.balls = EntityManager()
        self.balls.register_entity(self.ball)

    def create_texts(self):
        # create Pause entity
        self.pause_text = Pause("Press Space to Toggle Pause", TEXT_SIZE, WHITE)
        # create Score entities
        self.score1 = Score(self.player1.get_name() + " score: " + self.player1.get_score(),
                            SCORE_SIZE, WHITE)
        self.score2 = Score(self.player2.get_name() + " score: " + self.player2.get_score(),
                            SCORE_SIZE, WHITE)
        # register scores and pause entities with manager
        self.texts = EntityManager()
        self.texts.register_entity(self.pause_text)
        self.scores = EntityManager()
        self.scores.register_entity(self.score1)
        self.scores.register_entity(self.score2)

    def update_scores(self):
        self.score1.name = self.player1.get_name() + " score: " + self.player1.get_score()
        self.score2.name = self.player2.get_name() + " score: " + self.player2.get_score()
        self.score1.update_graphics()
        self.score2.update_graphics()

    def paddle_off_bounds_handler(self, player):
        player.components["graphics"].rect.top = max(player.components["graphics"].rect.top, 0)
        player.components["graphics"].rect.bottom = min(player.components["graphics"].rect.bottom, WIN_H)

    def ball_off_bounds_handler(self, ball):
        if ball.components["graphics"].rect.left <= 0:
            self.player2.increase_score(1)
            self.scored = True
        elif ball.components["graphics"].rect.right >= WIN_W:
            self.player1.increase_score(1)
            self.scored = True
        if ball.components["graphics"].rect.top <= 0 or ball.components["graphics"].rect.bottom >= GAME_H:
            ball.components["velocity"].y_velocity *= -1

    def exit_state(self):
        self.game.running = False
