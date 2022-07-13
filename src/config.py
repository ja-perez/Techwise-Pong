SCREEN_RESOLUTION = 200,300
TITLE = "PONG"
FPS = 60

DESIGN_RESOLUTION = 640, 480
PADDLE_RECT = DESIGN_RESOLUTION[0]/32, DESIGN_RESOLUTION[1]/6
PLAYER1_INITIAL_POS = PADDLE_RECT[0], (DESIGN_RESOLUTION[1]/2) - PADDLE_RECT[1]/2
PLAYER2_INITIAL_POS = (DESIGN_RESOLUTION[0] - (2 * PADDLE_RECT[0])), (DESIGN_RESOLUTION[1]/2) - PADDLE_RECT[1]/2

BALL_RECT = DESIGN_RESOLUTION[0]/80, DESIGN_RESOLUTION[1]/60
BALL_INITIAL_POS = ((DESIGN_RESOLUTION[0]/2)-BALL_RECT[0]/2, (DESIGN_RESOLUTION[1]/2)-BALL_RECT[1]/2)

SCORE1_POSITION = (DESIGN_RESOLUTION[0]/4) * 1, DESIGN_RESOLUTION[1]/16
SCORE2_POSITION = (DESIGN_RESOLUTION[0]/4) * 3, DESIGN_RESOLUTION[1]/16
SCORE_TEXT_SIZE = 60
SCORE_TEXT_COLOR = (255,255,255)