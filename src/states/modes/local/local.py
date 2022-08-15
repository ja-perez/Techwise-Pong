import pygame, random
from states.state import State
from Constants import *
from ecs.entities import Player, Ball, Score, Pause, Start
from ecs.entity_manager import EntityManager
from states.modes.local.localcommands import LocalCommand, up_command, down_command, set_pause, set_start, set_exit
from commands.command import ActiveOn
from ecs.systems import draw_system, move_system, collision_detection_system, ai_system
from pygame import mixer

class Local(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.start, self.pause = False, False
        self.left_paddle_color = WHITE
        self.right_paddle_color = WHITE
        self.game_mode = 2
        self.scored, self.collision_present, self.volley, self.boost = False, False, 1, 2
        self.register_commands()
        self.create_entities()
        self.next_state = ""

    def set_game_mode(self, number):
        self.game_mode = number
    
    def update(self):
        command_queue = self.ih.handle_input()
        for command, args in command_queue:
            command.execute(args[0])
        if self.start:
            self.p1_y_direction = self.p1_down - self.p1_up
            self.p2_y_direction = self.p2_down - self.p2_up

            if self.game_mode == 0:
                move_system(self.player1, self.paddle_off_bounds_handler, 0, self.p1_y_direction)
                move_system(self.player2, self.paddle_off_bounds_handler, 0, self.p2_y_direction)
            if self.game_mode == 1:
                move_system(self.player1, self.paddle_off_bounds_handler, 0, self.p1_y_direction)
                ai_system(self.player2, self.ball, self.paddle_off_bounds_handler, 0)
            if self.game_mode == 2:
                ai_system(self.player1, self.ball, self.paddle_off_bounds_handler, 0)
                ai_system(self.player2, self.ball, self.paddle_off_bounds_handler, 0)

            move_system(self.ball, self.ball_off_bounds_handler, self.ball_x_dir, self.ball_y_dir)
            self.update_score()
            self.collision_present = collision_detection_system(
                self.ball, self.g_manager.all_active_component_instances("graphics"))
            self.collision_handler(self.collision_present)
        if self.pause:
            self.next_state = "pause"
            self.change_state(self.next_state)
        self.update_colors()

    def render(self):
        if not self.start:
            self.game.screen.blit(self.start_text.components["graphics"].surface,
                                  self.start_text.components["graphics"].rect)
            draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))
        else:
            self.game.screen.blit(self.pause_text.components["graphics"].surface,
                                  self.pause_text.components["graphics"].rect)
            draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))

    def register_commands(self):
        # Command: press p to pause and transition to pause state
        self.pause_command = LocalCommand(ActiveOn.PRESSED, set_pause, self)
        self.ih.register_command(pygame.K_p, self.pause_command)
        # Command: press space to start
        self.start_command = LocalCommand(ActiveOn.PRESSED, set_start, self)
        self.ih.register_command(pygame.K_SPACE, self.start_command)
        # Command: press esc to exit game
        self.exit_command = LocalCommand(ActiveOn.PRESSED, set_exit, self)
        self.ih.register_command(pygame.K_ESCAPE, self.exit_command)
        # Command: press up/w to move player up and down/s to move player down
        self.player_up_press = LocalCommand(ActiveOn.BOTH, up_command, self)
        self.player_down_press = LocalCommand(ActiveOn.BOTH, down_command, self)
        # Player 1 movement
        self.ih.register_command(pygame.K_w, self.player_up_press)
        self.ih.register_command(pygame.K_s, self.player_down_press)
        # Player 2 movement
        self.ih.register_command(pygame.K_UP, self.player_up_press)
        self.ih.register_command(pygame.K_DOWN, self.player_down_press)

    def create_entities(self):
        self.g_manager = EntityManager()
        self.create_players()
        self.create_balls()
        self.create_texts()
        self.set_start_positions()

    def set_start_positions(self):
        self.player1.set_pos(BALL[0], GAME_H - PADDLE[1] / 2)
        self.player2.set_pos(GAME_W * 2 - PADDLE[0] - BALL[0], GAME_H - PADDLE[1] / 2)
        # self.ball.set_pos(GAME_W, GAME_H - BALL[1] / 2)
        self.start_text.set_pos(GAME_W - self.start_text.components["graphics"].rect.width / 2,
                                self.start_text.components["graphics"].rect.height * 2)
        self.pause_text.set_pos(0, GAME_H * 2 - self.pause_text.components["graphics"].rect.height)
        self.score1.set_pos(self.player1.surface.get_width() * 2, 0)
        self.score2.set_pos(GAME_W * 2 - self.score2.surface.get_width() * 1.5, 0)

    def set_left_paddle_color(self, color):
        self.left_paddle_color = color

    def set_right_paddle_color(self, color):
        self.right_paddle_color = color

    def update_colors(self):
        self.player1.set_color(self.left_paddle_color)
        self.player2.set_color(self.right_paddle_color)

    def create_players(self):
        # create player 1:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        # set up and down values to false and direction to 0
        # set color based on settings menu color selection
        self.player1 = Player("player 1")
        self.player1.set_vel(0, 10)
        self.p1_up, self.p1_down = False, False
        self.p1_y_direction = 0
        self.player1.set_color(self.left_paddle_color)
        # create player 2:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        # set up and down values to false and direction to 0
        # set color based on settings menu color selection
        self.player2 = Player("player 2")
        self.player2.set_vel(0, 10)
        self.p2_up, self.p2_down = False, False
        self.p2_y_direction = 0
        self.player2.set_color(self.right_paddle_color)
        # register both players with game manager
        self.g_manager.register_entity(self.player1)
        self.g_manager.register_entity(self.player2)

    def create_balls(self):
        # create ball and set position to the center of the screen
        self.ball = Ball("ball")
        self.ball.set_pos(GAME_W, GAME_H - BALL[1] / 2)
        self.ball_vel = 6
        self.ball_x_dir = 1 if random.randint(0, 1) else -1
        self.ball_y_dir = 1 if random.randint(0, 1) else -1
        self.ball.set_vel(self.ball_vel, self.ball_vel)
        # register ball with game manager
        self.g_manager.register_entity(self.ball)

    def create_texts(self):
        # create Pause entity
        self.pause_text = Pause("Press P to Toggle Pause", SCORE_SIZE, WHITE)
        # create Start entity
        self.start_text = Start("Press Space to Start", TEXT_SIZE, WHITE)
        # create Score entities
        self.score1 = Score(self.player1.get_name() + " score: " + self.player1.get_score(),
                            SCORE_SIZE, WHITE)
        self.score2 = Score(self.player2.get_name() + " score: " + self.player2.get_score(),
                            SCORE_SIZE, WHITE)
        # register scores with game manager and pause with text manager
        self.g_manager.register_entity(self.score1)
        self.g_manager.register_entity(self.score2)

    def update_score(self):
        if self.scored:
            self.g_manager.unregister_entity(self.ball)
            self.create_balls()
            self.scored = False
            self.score1.name = self.player1.get_name() + " score: " + self.player1.get_score()
            self.score2.name = self.player2.get_name() + " score: " + self.player2.get_score()
            self.score1.update_graphics()
            self.score2.update_graphics()
            self.volley = 1

    def paddle_off_bounds_handler(self, player):
        player.components["graphics"].rect.top = max(player.components["graphics"].rect.top, 0)
        player.components["graphics"].rect.bottom = min(player.components["graphics"].rect.bottom, WIN_H)

    def ball_off_bounds_handler(self, ball):
        #SOUNDS MOVE LATER
        pointfx = mixer.Sound("point.wav")
        bouncefx = mixer.Sound("bounce.wav")
        bouncefx.set_volume(0.3)
        pointfx.set_volume(0.4)

        if ball.components["graphics"].rect.left <= 0:
            self.player2.increase_score(1)
            self.scored = True
            pointfx.play()
        elif ball.components["graphics"].rect.right >= WIN_W:
            self.player1.increase_score(1)
            self.scored = True
            pointfx.play()
        if ball.components["graphics"].rect.top <= 0 or ball.components["graphics"].rect.bottom >= WIN_H:
            self.ball_y_dir *= -1
            bouncefx.play()

    def collision_handler(self, collision_present):
        # SOUND MOVE LATER
        bouncefx = mixer.Sound("bounce.wav")
        bouncefx.set_volume(0.3)

        if collision_present:
            self.ball_x_dir *= -1
            self.volley += 1
            bouncefx.play()

            ## COMMENTED OUT FOR FASTER VOLLEY
            # if self.volley % self.boost == 0:
            #     self.ball.set_vel(self.ball.x_vel() + self.volley / 2.5, self.ball.y_vel() + self.volley / 2.5)

            # Faster Volley
            self.ball.set_vel(self.ball.x_vel() + 2, self.ball.y_vel() + 2)


            # GAME MODE STUFF - FIX LATER
            #self.ball.increase_radius(6)
            self.player1.change_size(1, 1)
            self.player2.change_size(1, 1)


    def exit_state(self):
        if self.pause:
            self.pause = False
