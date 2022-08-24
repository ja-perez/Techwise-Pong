from Constants import *
from pygame import mixer

class Themes():
    def __init__(self):
        self.classic()

    def set_vfx_volume(self, bounce_vol, score_vol):
        self.bounce_vfx = mixer.Sound(self.bounce)
        self.score_vfx = mixer.Sound(self.score)
        self.bounce_volume = bounce_vol
        self.score_volume = score_vol
        self.bounce_vfx.set_volume(self.bounce_volume)
        self.score_vfx.set_volume(self.score_volume)

    def set_bounce_volume(self, value):
        if value == 0:
            self.bounce_vfx.set_volume(0)
        else:
            self.bounce_vfx.set_volume(self.bounce_volume)

    def set_score_volume(self, value):
        if value == 0:
            self.score_vfx.set_volume(0)
        else:
            self.score_vfx.set_volume(self.score_volume)


    def classic(self):
        self.background_color = BLACK
        self.background_music = "sounds/background/classic_bgm.wav"
        self.bounce = "sounds/bounce/classic_bounce.wav"
        self.score = "sounds/score/classic_score.wav"
        self.left_paddle_color = WHITE
        self.right_paddle_color = WHITE
        self.ball_image = "themes/ball_images/classic_ball.png"
        self.set_vfx_volume(0.3, 0.3)

    def cyberpunk(self):
        self.background_color = "themes/backgrounds/cyberpunk.jpg"
        self.background_music = "sounds/background/cyberpunk_bgm.wav"
        self.bounce = "sounds/bounce/cyberpunk_bounce.wav"
        self.score = "sounds/score/cyberpunk_score.wav"
        self.left_paddle_color = CYBERPUNK_1
        self.right_paddle_color = CYBERPUNK_2
        self.ball_image = "themes/ball_images/cyberpunk_ball.png"
        self.set_vfx_volume(0.7, 0.7)

    def disco(self):
        self.background_color = "themes/backgrounds/disco2.jpg"
        self.background_music = "sounds/background/disco_bgm.wav"
        self.bounce = "sounds/bounce/disco_bounce.wav"
        self.score = "sounds/score/classic_score.wav"
        self.left_paddle_color = DISCO_1
        self.right_paddle_color = DISCO_2
        self.ball_image = "themes/ball_images/disco_ball.png"
        self.set_vfx_volume(0.3, 0.3)

    def science(self):
        self.background_color = "themes/backgrounds/science.jpg"
        self.background_music = "sounds/background/science_bgm.wav"
        self.bounce = "sounds/bounce/science_bounce.wav"
        self.score = "sounds/score/science_score.wav"
        self.left_paddle_color = SCIENCE_1
        self.right_paddle_color = SCIENCE_2
        self.ball_image = "themes/ball_images/science_ball.png"
        self.set_vfx_volume(0.3, 0.3)

    def snow(self):
        self.background_color = "themes/backgrounds/snow.jpg"
        self.background_music = "sounds/background/snow_bgm.wav"
        self.bounce = "sounds/bounce/snow_bounce.wav"
        self.score = "sounds/score/snow_score.wav"
        self.left_paddle_color = SNOW_1
        self.right_paddle_color = SNOW_2
        self.ball_image = "themes/ball_images/snow_ball.png"
        self.set_vfx_volume(0.3, 0.3)

    def western(self):
        self.background_color = "themes/backgrounds/western.jpg"
        self.background_music = "sounds/background/western_bgm.wav"
        self.bounce = "sounds/bounce/western_bounce.wav"
        self.score = "sounds/score/western_score.wav"
        self.left_paddle_color = WESTERN_1
        self.right_paddle_color = WESTERN_2
        self.ball_image = "themes/ball_images/western_ball.png"
        self.set_vfx_volume(0.3, 0.3)