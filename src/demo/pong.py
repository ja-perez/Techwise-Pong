import random
import pygame
import ecs
import sys

from config import *
from globals import *

def init_display():
    global g_screen
    global g_background

    g_screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption(TITLE)

    g_background = pygame.Surface(DESIGN_RESOLUTION)
    g_background.fill((0,0,0))
    g_screen.blit(pygame.transform.scale(g_background, SCREEN_RESOLUTION), (0,0))
    pygame.display.flip()

def init_game():
    register_players()
    register_ball()
    register_hud()

def game_loop():
    global g_screen
    global g_background
    global g_entities_manager

    global g_ball
    global g_clock
    global g_player1
    global g_player2
    global g_score1
    global g_score2

    dirty_rects = list()
    design_surface = pygame.Surface(DESIGN_RESOLUTION)
    design_surface.fill((0,0,0))
    
    paddle_off_bounds_handler = get_paddle_off_bounds_handler(design_surface.get_height())
    ball_off_bounds_handler = get_ball_off_bounds_handler(design_surface, g_background, dirty_rects, g_score1, g_score2, g_background.get_height())
    ball_collision_handler = get_ball_collision_handler(g_ball)
    
    while True:
        input = process_input(design_surface, dirty_rects)
        ecs.erase_system(design_surface, g_background, g_entities_manager.get_all_instances_of_component_class("GraphicComponent"), dirty_rects)
        p1_y_direction = input[pygame.K_s] - input[pygame.K_w]
        if p1_y_direction != 0:
            ecs.move_system((g_player1,), paddle_off_bounds_handler, p1_y_direction)
        
        p2_y_direction = input[pygame.K_DOWN] - input[pygame.K_UP]
        if p2_y_direction != 0:
            ecs.move_system((g_player2,), paddle_off_bounds_handler, p2_y_direction)
        
        score_before = set(g_score)
        ecs.move_system((g_ball,), ball_off_bounds_handler)
        if set(g_score) != score_before:
            ecs.erase_system(design_surface, g_background, [g_ball["GraphicComponent"]], dirty_rects)
            register_ball()

        ecs.collision_detection_with_handling_system(g_ball, [g_player1,g_player2], g_entities_manager, ball_collision_handler)
        ecs.draw_system(design_surface, g_entities_manager.get_all_instances_of_component_class("GraphicComponent"), dirty_rects)
        
        g_screen.blit(pygame.transform.scale(design_surface, SCREEN_RESOLUTION), (0,0))
        pygame.display.flip()
        dirty_rects.clear()

        g_clock.tick(FPS)

def register_players():
    global g_player1
    global g_player2

    player_surface = pygame.Surface(PADDLE_RECT)
    player_surface.fill((255,255,255))

    g_player1["GraphicComponent"]  = ecs.GraphicComponent(player_surface, PLAYER1_INITIAL_POS[0], PLAYER1_INITIAL_POS[1])
    g_player1["VelocityComponent"] = ecs.VelocityComponent(0, 10)
    g_entities_manager.register_entity(g_player1)

    g_player2["GraphicComponent"]  = ecs.GraphicComponent(player_surface, PLAYER2_INITIAL_POS[0], PLAYER2_INITIAL_POS[1])
    g_player2["VelocityComponent"] = ecs.VelocityComponent(0, 10)
    g_entities_manager.register_entity(g_player2)

def register_ball():
    global g_ball

    random.seed()
    ball_surface = pygame.Surface((BALL_RECT))
    ball_surface.fill((255,255,255))

    g_ball["GraphicComponent"] = ecs.GraphicComponent(ball_surface, BALL_INITIAL_POS[0], BALL_INITIAL_POS[1])
    g_ball["VelocityComponent"] = ecs.VelocityComponent(random.randint(5,8) *(1 if random.randint(0,1) else -1), random.randint(5,8)*(1 if random.randint(0,1) else -1))
    g_entities_manager.register_and_enlist_entity(g_ball, "ball")

def register_hud():
    global g_score1
    global g_score2

    g_score1["TextComponent"] = ecs.TextComponent("{}".format(0), SCORE_TEXT_SIZE, SCORE_TEXT_COLOR)
    score_surface1 = g_score1["TextComponent"].font.render(g_score1["TextComponent"].text, False, g_score1["TextComponent"].color)
    g_score1["GraphicComponent"] = ecs.GraphicComponent(score_surface1, SCORE1_POSITION[0], SCORE1_POSITION[1]) 
    g_entities_manager.register_entity(g_score1)

    g_score2["TextComponent"] = ecs.TextComponent("{}".format(0), SCORE_TEXT_SIZE, SCORE_TEXT_COLOR)
    score_surface2 = g_score2["TextComponent"].font.render(g_score2["TextComponent"].text, False, g_score1["TextComponent"].color)
    g_score2["GraphicComponent"] = ecs.GraphicComponent(score_surface2, SCORE2_POSITION[0], SCORE2_POSITION[1])
    g_entities_manager.register_entity(g_score2)

def get_paddle_off_bounds_handler(bottom_edge: int):
    def paddle_off_bounds_handler(player: ecs.Entity):
        player["GraphicComponent"].rect.top = max(player["GraphicComponent"].rect.top, 0)
        player["GraphicComponent"].rect.bottom = min(player["GraphicComponent"].rect.bottom, bottom_edge)
    return paddle_off_bounds_handler

def get_ball_collision_handler(ball: ecs.Entity):
    def ball_collision_handler(collided_entities, collided_entity_idx, entities_manager):
        x_vel = ball["VelocityComponent"].x_velocity
        ball["VelocityComponent"].x_velocity = (x_vel + 1) * -1 if x_vel > 0 else (x_vel -1)* -1
    return ball_collision_handler

def get_ball_off_bounds_handler(screen: pygame.Surface, background: pygame.Surface, dirty_rects, score1: ecs.Entity, score2: ecs.Entity, bottom_edge: int):
    def ball_off_bounds_handler(ball: ecs.Entity):
        global g_score
        if ball["GraphicComponent"].rect.top <= 0 or ball["GraphicComponent"].rect.bottom >= bottom_edge:
            ball["VelocityComponent"].y_velocity *= -1
        if ball["GraphicComponent"].rect.left <= 0:
            g_score = (g_score[0], g_score[1]+1)
            ecs.rewrite_text_system(screen, background, dirty_rects, score2, "{}".format(g_score[1]))
        if ball["GraphicComponent"].rect.right >= background.get_width():
            g_score = (g_score[0]+1, g_score[1])
            ecs.rewrite_text_system(screen, background, dirty_rects, score1, "{}".format(g_score[0]))
    return ball_off_bounds_handler

def process_input(design_surface, dirty_rects):
    global g_score
    pygame.event.pump()
    input = pygame.key.get_pressed()
    if input[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        pygame.quit()
    elif input[pygame.K_p]:
        while True:
            pygame.event.pump()
            input = pygame.key.get_pressed()
            if input[pygame.K_u]:
                break
            g_clock.tick(FPS)
    elif input[pygame.K_r]:
        ecs.erase_system(design_surface, g_background, [g_ball["GraphicComponent"]], dirty_rects)
        g_score = 0, 0
        ecs.rewrite_text_system(design_surface, g_background, dirty_rects, g_score2, "{}".format(g_score[1]))
        ecs.rewrite_text_system(design_surface, g_background, dirty_rects, g_score1, "{}".format(g_score[0]))
        register_ball()
    return input

def main():
    pygame.init()

    init_display()
    init_game()
    game_loop()
    
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()