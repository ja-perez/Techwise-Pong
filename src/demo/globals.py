import pygame
import ecs

g_screen = pygame.Surface((0,0))
g_background = pygame.Surface((0,0))
g_entities_manager = ecs.EntitiesManager()
g_clock = pygame.time.Clock()
g_player1,g_player2,g_ball,g_score1, g_score2 = dict(),dict(),dict(),dict(),dict()
g_score = 0,0