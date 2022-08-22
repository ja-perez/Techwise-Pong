import pygame, random, pygwidgets
from states.state import State
from Constants import *
from ecs.entities import Player, Ball, Score, Pause, Start, State_Text
from ecs.entity_manager import EntityManager
from states.modes.local.localcommands import LocalCommand, up_command, down_command, set_pause, set_start, set_exit
from commands.command import ActiveOn
from ecs.systems import draw_system, move_system, collision_detection_system, ai_system
from pygame import mixer
from themes.themes import Themes

class Local(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.start, self.pause = False, False
        self.themes = Themes()
        # Game Modes - 0: Classic, 1: Frenzy, 2: Low-Grav, 3: TTA
        # Player Pairs - 0: Player v. Player, 1: Player v. AI, 2: AI v. AI
        self.game_mode, self.player_pair = 0, 2
        #TO USE CLASSIC TURN ON THIS BOOL
        self.classic_bool = False
        self.left_paddle_color = self.themes.left_paddle_color
        self.right_paddle_color = self.themes.right_paddle_color

        self.scored, self.winning_score, self.winner = False, 2, ""
        self.collision_present, self.volley, self.boost = False, 0, 2
        self.register_commands()
        self.create_entities()
        self.next_state = ""
        self.teleport = 1

        # Use to change theme. Available themes are: classic, cyberpunk, disco, science, snow, and western
        # (Will add to its own theme settings menu later)

        #self.themes.snow()
        self.themes.disco()

        #used to edit background color in game.py
        if not self.classic_bool:
            self.background_color = pygame.image.load(self.themes.background_color)
        else:
            self.background_color = self.themes.background_color

    def set_game_mode(self, number):
        self.game_mode = number

    def set_player_pair(self, number):
        self.player_pair = number

    def update(self):
        if self.winner:
            # print Game Over, Player X is the winner!
            # Return to main menu button
            for event in pygame.event.get():
                if self.homemenu_btn.handleEvent(event):
                    self.next_state = "mainmenu"
                    self.change_state(self.next_state)
        else:
            command_queue = self.ih.handle_input()
            for command, args in command_queue:
                command.execute(args[0])
            if self.start:
                self.p1_y_direction = self.p1_down - self.p1_up
                self.p2_y_direction = self.p2_down - self.p2_up

                if self.player_pair == 0:
                    move_system(self.player1, self.paddle_off_bounds_handler, 0, self.p1_y_direction)
                    move_system(self.player2, self.paddle_off_bounds_handler, 0, self.p2_y_direction)
                if self.player_pair == 1:
                    move_system(self.player1, self.paddle_off_bounds_handler, 0, self.p1_y_direction)
                    ai_system(self.player2, self.ball, self.paddle_off_bounds_handler, 0)
                if self.player_pair == 2:
                    ai_system(self.player1, self.ball, self.paddle_off_bounds_handler, 0)
                    ai_system(self.player2, self.ball, self.paddle_off_bounds_handler, 0)

                move_system(self.ball, self.ball_off_bounds_handler, self.ball_x_dir, self.ball_y_dir)
                self.update_score()
                self.collision_present = collision_detection_system(
                    self.ball, self.g_manager.all_active_component_instances("graphics"))
                self.collision_handler(self.collision_present)
            elif self.pause:
                self.next_state = "pause"
                self.change_state(self.next_state)

        # temp Through the Ages game mode logic
        if self.game_mode == 3 and self.collision_present:
            # Start at snow -> western -> disco -> science -> cyberpunk
            if self.volley == 2:
                self.themes.western()
                self.update_theme()
            elif self.volley == 4:
                self.themes.disco()
                self.update_theme()
            elif self.volley == 4:
                self.themes.science()
                self.update_theme()
            elif self.volley == 4:
                self.themes.cyberpunk()
                self.update_theme()
        self.update_colors()

    def update_theme(self):
        self.background_color = pygame.image.load(self.themes.background_color)
        self.game.background = self.background_color
        self.game.change_music()

    def render(self):
        if self.winner:
            self.winner_text.name = "Game Over, " + self.winner + " is the winner!"
            self.winner_text.update_surface()
            self.winner_text.update_graphics()
            self.winner_text.set_coords(GAME_W - self.winner_text.get_width(), GAME_H / 2)
            self.game.screen.blit(self.winner_text.components["graphics"].surface,
                                  self.winner_text.components["graphics"].rect)
            self.homemenu_btn.draw()
        else:
            if not self.start:
                self.game.screen.blit(self.start_text.components["graphics"].surface,
                                      self.start_text.components["graphics"].rect)
            else:
                self.game.screen.blit(self.pause_text.components["graphics"].surface,
                                      self.pause_text.components["graphics"].rect)
            draw_system(self.game.screen, self.g_manager.all_component_instances("graphics"))
            ball_pos = self.ball.get_cords()[0] - self.ball_image.get_width() // 2, self.ball.get_cords()[1] \
                       - self.ball_image.get_height() // 2
            self.game.screen.blit(self.ball_image, ball_pos)
        # surface = pygame.Surface((30, 30))
        # ball_image = pygame.Surface.convert(pygame.image.load('themes/ball_images/disco_ball.png'))
        # pygame.Surface.blit(surface, self.game.screen, (100, 100))


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
        self.player1 = Player("Player 1")
        self.player1.set_vel(0, 10)
        self.p1_up, self.p1_down = False, False
        self.p1_y_direction = 0
        self.player1.set_color(self.left_paddle_color)
        # create player 2:
        # set position to the left of the screen
        # set x velocity to 0 and y velocity to 10
        # set up and down values to false and direction to 0
        # set color based on settings menu color selection
        self.player2 = Player("Player 2")
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

        self.ball_image = pygame.Surface.convert(pygame.image.load("themes\\ball_images\\disco_ball.png"), self.ball.components["graphics"].surface)
        self.ball_image = pygame.transform.scale(self.ball_image, BALL)

        # self.surface.blit(self.ball_image, self.ball.get_surface, GAME_W, GAME_H - BALL[1] / 2)

        #if not self.classic_bool:
        # pygame.Surface.blit(self.ball_image, self.ball.components["graphics"].surface, (GAME_W, GAME_H - BALL[1] / 2))
        #pygame.Surface.blit(ball_image, self.game.screen, (GAME_W, GAME_H - BALL[1] / 2))

    def create_texts(self):
        # create Winner entity
        self.winner_text = State_Text("Game Over", TEXT_SIZE, WHITE, FONT_NAME)
        # create Pause entity
        self.pause_text = Pause("Press P to Toggle Pause", SCORE_SIZE, WHITE, FONT_NAME)
        # create Start entity
        self.start_text = Start("Press Space to Start", TEXT_SIZE, WHITE, FONT_NAME)
        # create Score entities
        self.score1 = Score(self.player1.get_name() + " score: " + self.player1.get_score(),
                            SCORE_SIZE, WHITE, FONT_NAME)
        self.score2 = Score(self.player2.get_name() + " score: " + self.player2.get_score(),
                            SCORE_SIZE, WHITE, FONT_NAME)
        # register scores with game manager and pause with text manager
        self.g_manager.register_entity(self.score1)
        self.g_manager.register_entity(self.score2)

        self.homemenu_btn = pygwidgets.TextButton(self.game.screen, (0, 0), "Return to Main Menu",
                                                  fontSize=MENU_FONT_SIZE, fontName=FONT_NAME,
                                                  width=200, height=50)
        self.homemenu_btn.moveXY(GAME_W - 200/2, GAME_H - 50/2)

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
            if self.winning_score == int(self.player1.get_score()):
                self.winner = self.player1.get_name()
            elif self.winning_score == int(self.player2.get_score()):
                self.winner = self.player2.get_name()

    def paddle_off_bounds_handler(self, player):
        player.components["graphics"].rect.top = max(player.components["graphics"].rect.top, 0)
        player.components["graphics"].rect.bottom = min(player.components["graphics"].rect.bottom, WIN_H)

    def ball_off_bounds_handler(self, ball):


        if ball.components["graphics"].rect.left <= 0:
            self.player2.increase_score(1)
            self.scored = True
            self.themes.score_vfx.play()
        elif ball.components["graphics"].rect.right >= WIN_W:
            self.player1.increase_score(1)
            self.scored = True
            self.themes.score_vfx.play()
        if ball.components["graphics"].rect.top <= 0 or ball.components["graphics"].rect.bottom >= WIN_H:
            self.ball_y_dir *= -1
            self.themes.bounce_vfx.play()

    def collision_handler(self, collision_present):

        if collision_present:
            self.ball_x_dir *= -1
            self.volley += 1
            self.themes.bounce_vfx.play()

            ## COMMENTED OUT FOR FASTER VOLLEY
            # if self.volley % self.boost == 0:
            #     self.ball.set_vel(self.ball.x_vel() + self.volley / 2.5, self.ball.y_vel() + self.volley / 2.5)

            # Faster Volley
            # Frenzy game mode
            if self.game_mode == 1:
                self.ball.set_vel(self.ball.x_vel() + 2, self.ball.y_vel() + 2)
            # Low gravity game mode
            elif self.game_mode == 2:
                self.ball.set_vel(self.ball.x_vel() - 0.25, self.ball.y_vel() - 0.25)
                self.player1.set_vel(0, self.player1.get_y_vel() - 0.25)
                self.player2.set_vel(0, self.player2.get_y_vel() - 0.25)
            # GAME MODE STUFF - FIX LATER
            # self.ball.increase_radius(6)
            self.player1.change_size(1, 1)
            self.player2.change_size(1, 1)
            # self.teleport += 1
            # if self.teleport == 3:
            #     self.ball.set_pos(random.randrange(400, 520), GAME_H - BALL[1] / 2)
            #     self.teleport = 1

            # Generate random colors
            self.random_color1 = random.choices(range(256), k=3)
            self.random_color2 = random.choices(range(256), k=3)

            # Turn on random color flag - Used to turn backgrounds color
            self.random_color_flag = True

            # Change Paddle color on paddle hit
            # self.set_right_paddle_color(self.random_color1)
            # self.set_left_paddle_color(self.random_color2)

            # Change backgrounds color on paddle hit
            # if self.random_color_flag:
            #     self.game.change_background_color()

    def enter_state(self):
        if self.game_mode == 3:
            self.classic_bool = False
            self.themes.snow()
            self.background_color = pygame.image.load(self.themes.background_color)
            self.game.background = self.background_color
            self.game.change_music()

    def exit_state(self):
        if self.pause:
            self.pause = False
