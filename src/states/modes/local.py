import pygame
from states.state import State
from Constants import *
from ecs.entities import Player, Ball, Score
from ecs.entity_manager import EntityManager


class Local(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_players()
        self.create_balls()
        self.create_scoreboards()


    def update(self):
        pass

    def render(self):
        for player_graphic in self.players.component_to_entity["graphics"]:
            self.game.screen.blit(player_graphic.components["graphics"].surface,
                                  player_graphic.components["graphics"].rect)
        for ball_graphic in self.balls.component_to_entity["graphics"]:
            self.game.screen.blit(ball_graphic.components["graphics"].surface,
                                  ball_graphic.components["graphics"].rect)
        for score_graphic in self.scores.component_to_entity["graphics"]:
            self.game.screen.blit(score_graphic.components["graphics"].surface,
                                  score_graphic.components["graphics"].rect)

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
