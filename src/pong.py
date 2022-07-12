import random
import pygame
import ecs

RESOLUTION = 640, 480
TITLE = "PONG"
FPS = 60

PLAYER_INITIAL_POS = (20, RESOLUTION[1]/2)
COMPUTER_INITIAL_POS = (RESOLUTION[0]-40, RESOLUTION[1]/2)
BALL_INITIAL_POS = (RESOLUTION[0]/2, RESOLUTION[1]/2)

SCORE_POSITION = (RESOLUTION[0]/2, 1)
SCORE_TEXT_SIZE = 20
SCORE_TEXT_COLOR = "white"
SCORE = 0,0
class Score:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def run_game():
    screen = pygame.display.set_mode(RESOLUTION)
    screen_rect = screen.get_rect()

    pygame.display.set_caption(TITLE)
    background = pygame.Surface(screen_rect.size)

    background.fill((0,0,255))
    screen.blit(background, (0,0))
    pygame.display.flip()

    random.seed()
    game_loop(screen, background)


def register_player1(player_surface: pygame.Surface, entities_manager: ecs.EntitiesManager, player: ecs.Entity):
    player["GraphicComponent"] = ecs.GraphicComponent(player_surface, PLAYER_INITIAL_POS[0], PLAYER_INITIAL_POS[1])
    player["VelocityComponent"] = ecs.VelocityComponent(0, 10)
    entities_manager.register_entity(player)

def register_player2(computer_surface: pygame.Surface, entities_manager: ecs.EntitiesManager, computer: ecs.Entity):
    computer["GraphicComponent"] = ecs.GraphicComponent(computer_surface, COMPUTER_INITIAL_POS[0], COMPUTER_INITIAL_POS[1])
    computer["VelocityComponent"] = ecs.VelocityComponent(0, 10)
    entities_manager.register_entity(computer)

def register_ball(ball_surface: pygame.Surface, entities_manager: ecs.EntitiesManager, ball: ecs.Entity):
    ball["GraphicComponent"] = ecs.GraphicComponent(ball_surface, BALL_INITIAL_POS[0], BALL_INITIAL_POS[1])
    ball["VelocityComponent"] = ecs.VelocityComponent(random.randint(3,5), random.randint(3,5))
    entities_manager.register_and_enlist_entity(ball, "ball")

def register_score(entities_manager: ecs.EntitiesManager, score: ecs.Entity):
    score["TextComponent"] = ecs.TextComponent("Score: {} - {}".format(0,0), SCORE_TEXT_SIZE, SCORE_TEXT_COLOR)
    score_surface = score["TextComponent"].font.render(score["TextComponent"].text, False, score["TextComponent"].color)
    score["GraphicComponent"] = ecs.GraphicComponent(score_surface, SCORE_POSITION[0], SCORE_POSITION[1])
    entities_manager.register_entity(score)

def game_loop(screen: pygame.Surface, background: pygame.Surface):
    entities_manager = ecs.EntitiesManager()
    clock = pygame.time.Clock()

    player1, player2, ball_e, score = dict(), dict(), dict(), dict()
    dirty_rects = list()

    paddle = pygame.Surface((RESOLUTION[0]/30,RESOLUTION[1]/10))
    paddle.fill((255,255,255))

    ball = pygame.Surface((RESOLUTION[0]/40, RESOLUTION[1]/40))
    ball.fill((255,255,255))

    register_player1(paddle, entities_manager, player1)
    register_player2(paddle, entities_manager, player2)
    register_ball(ball, entities_manager, ball_e)
    register_score(entities_manager, score)

    paddle_off_bounds_handler = get_paddle_off_bounds_handler(background.get_height())
    ball_off_bounds_handler = get_ball_off_bounds_handler(screen, background, dirty_rects, score, background.get_height())
    ball_collision_handler = get_ball_collision_handler(ball_e)

    
    while True:
        pygame.event.pump()
        input = pygame.key.get_pressed()
        if input[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
            break
        elif input[pygame.K_r]:
            ecs.erase_system(screen, background, [ball_e["GraphicComponent"]], dirty_rects)
            register_ball(ball, entities_manager, ball_e)
        
        ecs.erase_system(screen, background, entities_manager.get_all_instances_of_component_class("GraphicComponent"), dirty_rects)

        p1_y_direction = input[pygame.K_s] - input[pygame.K_w]
        if p1_y_direction != 0:
            ecs.move_system((player1,), paddle_off_bounds_handler, p1_y_direction)
        
        p2_y_direction = input[pygame.K_DOWN] - input[pygame.K_UP]
        if p2_y_direction != 0:
            ecs.move_system((player2,), paddle_off_bounds_handler, p2_y_direction)

        score_before = set(SCORE)
        ecs.move_system((ball_e,), ball_off_bounds_handler)
        if set(SCORE) != score_before:
            ecs.erase_system(screen, background, [ball_e["GraphicComponent"]], dirty_rects)
            register_ball(ball, entities_manager, ball_e)

        ecs.collision_detection_with_handling_system(ball_e, [player1,player2], entities_manager, ball_collision_handler)
        ecs.draw_system(screen, entities_manager.get_all_instances_of_component_class("GraphicComponent"), dirty_rects)
        pygame.display.update(dirty_rects)
        dirty_rects.clear()

        clock.tick(FPS)

def get_paddle_off_bounds_handler(bottom_edge: int):
    def paddle_off_bounds_handler(player: ecs.Entity):
        player["GraphicComponent"].rect.top = max(player["GraphicComponent"].rect.top, 0)
        player["GraphicComponent"].rect.bottom = min(player["GraphicComponent"].rect.bottom, bottom_edge)
    return paddle_off_bounds_handler

def get_ball_off_bounds_handler(screen: pygame.Surface, background: pygame.Surface, dirty_rects, score: ecs.Entity, bottom_edge: int):
    def ball_off_bounds_handler(ball: ecs.Entity):
        global SCORE
        if ball["GraphicComponent"].rect.top <= 0 or ball["GraphicComponent"].rect.bottom >= bottom_edge:
            ball["VelocityComponent"].y_velocity *= -1
        if ball["GraphicComponent"].rect.left <= 0:
            SCORE = (SCORE[0], SCORE[1]+1)
            ecs.rewrite_text_system(screen, background, dirty_rects, score, "Score: {} - {}".format(SCORE[0], SCORE[1]))
        if ball["GraphicComponent"].rect.right >= background.get_width():
            SCORE = (SCORE[0]+1, SCORE[1])
            ecs.rewrite_text_system(screen, background, dirty_rects, score, "Score: {} - {}".format(SCORE[0], SCORE[1]))
    return ball_off_bounds_handler

def get_ball_collision_handler(ball: ecs.Entity):
    def ball_collision_handler(collided_entities, collided_entity_idx, entities_manager):
        x_vel = ball["VelocityComponent"].x_velocity
        ball["VelocityComponent"].x_velocity = (x_vel + 1) * -1 if x_vel > 0 else (x_vel -1)* -1
    return ball_collision_handler


def main():
    pygame.init()
    run_game()
    pygame.quit()

if __name__=='__main__':
    main()