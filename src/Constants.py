import os
# assets path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

# GRAPHICS
WIN_W = 960
WIN_H = 540
GAME_W = 480
GAME_H = 270
GAME_TITLE = "Real-Time Pong Demo"
FONT_NAME = os.path.join(ASSETS_PATH, "fonts", 'Teko-Light.ttf')
CYBER_FONT = os.path.join(ASSETS_PATH, "fonts", 'neon_font.ttf')
FONT_SIZE = 100
MENU_FONT_SIZE = 20
SCORE_SIZE = 25
TEXT_SIZE = 40
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OLIVE_GREEN = (22, 110, 74)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

DISCO_1 = (160, 28, 163)
DISCO_2 = (75, 191, 230)

CYBERPUNK_1 = (255, 158, 199)
CYBERPUNK_2 = (165, 12, 93)

SNOW_1 = (140, 168, 181)
SNOW_2 = (110, 155, 181)

SCIENCE_1 = (224, 119, 6)
SCIENCE_2 = (17, 42, 70)

WESTERN_1 = (101, 30, 34)
WESTERN_2 = (244, 186, 63)

# OBJECT SIZES
PADDLE = WIN_W / 48, WIN_H / 5
PADDLE_W = WIN_W / 48
PADDLE_H = WIN_H / 5
BALL = WIN_W / 60 + 10, WIN_H / 35 + 10
BALL_W = WIN_W / 60 + 10
BALL_H = WIN_H / 35 + 10
BALL_RADIUS = GAME_W / 60

X = 0
Y = 0