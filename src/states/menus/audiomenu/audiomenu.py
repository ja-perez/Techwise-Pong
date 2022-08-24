import pygwidgets
import pygame
from states.state import State
from Constants import *
from commands.command import *
from input.input_handler import *

class AudioMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_audio_rb()
        self.create_audio_dt()
        self.create_return_button()
        self.move_rbs()
        self.move_dt()
        self.return_state = ""
        self.theme_name = 'classic'

    def update(self):
        for event in pygame.event.get():

            if self.music_on_rb.handleEvent(event):

                pygame.mixer.music.unpause()

            if self.music_off_rb.handleEvent(event):
                pygame.mixer.music.pause()

            if self.bounce_vfx_on_rb.handleEvent(event):
                self.game.states["local"].bounce_vfx_bool = True
            if self.bounce_vfx_off_rb.handleEvent(event):
                self.game.states["local"].bounce_vfx_bool = False

            if self.score_vfx_on_rb.handleEvent(event):
                self.game.states["local"].score_vfx_bool = True

            if self.score_vfx_off_rb.handleEvent(event):
                self.game.states["local"].score_vfx_bool = False

            if self.return_button.handleEvent(event):
                self.change_state(self.return_state)


    def render(self):
        self.button_display()
        #self.title_text()

    def button_display(self):
        #RADIO BUTTONS
        self.music_on_rb.draw()
        self.music_off_rb.draw()
        self.bounce_vfx_on_rb.draw()
        self.bounce_vfx_off_rb.draw()
        self.score_vfx_on_rb.draw()
        self.score_vfx_off_rb.draw()
        #DISPLAY TEXT
        self.title_text.draw()
        self.music_on_dt.draw()
        self.music_off_dt.draw()
        self.bounce_vfx_on_dt.draw()
        self.bounce_vfx_off_dt.draw()
        self.score_vfx_on_dt.draw()
        self.score_vfx_off_dt.draw()

        #RETURN BUTTON
        self.return_button.draw()

    def create_audio_rb(self):
        height_var = 50
        width_var = 50
        font_size = 1
        self.music_on_rb = pygwidgets.TextRadioButton(window=self.game.screen,
                                                     loc=(GAME_W, GAME_H),
                                                     group='music',
                                                     text='Classic',
                                                     fontName=FONT_NAME,
                                                     fontSize=font_size)
        self.music_on_rb.setValue(True)
        self.music_off_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                       group='music',
                                                       text='Cyberpunk',
                                                       fontName='neon_font.ttf',
                                                       fontSize=font_size)
        self.bounce_vfx_on_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                   group='bounce',
                                                   text='Disco',
                                                   fontName=FONT_NAME,
                                                   fontSize=font_size)
        self.bounce_vfx_on_rb.setValue(True)
        self.bounce_vfx_off_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                     group='bounce',
                                                     text='Science',
                                                     fontName=FONT_NAME,
                                                     fontSize=font_size)
        self.score_vfx_on_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                  group='score',
                                                  text='Snow',
                                                  fontName=FONT_NAME,
                                                  fontSize=font_size)
        self.score_vfx_on_rb.setValue(True)
        self.score_vfx_off_rb = pygwidgets.TextRadioButton(self.game.screen,(GAME_W, GAME_H),
                                                     group='score',
                                                     text='Western',
                                                     fontName=FONT_NAME,
                                                     fontSize=font_size)
    def create_audio_dt(self):
        self.title_text = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H//2 - 80),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)

        self.music_on_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.music_off_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.bounce_vfx_on_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)



        self.bounce_vfx_off_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.score_vfx_on_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.score_vfx_off_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)

        self.title_text.setText("Audio Menu")
        self.music_on_dt.setValue('Music On')
        self.music_off_dt.setValue('Music Off')
        self.bounce_vfx_on_dt.setValue('Bounce VFX On')
        self.bounce_vfx_off_dt.setValue('Bounce VFX Off')
        self.score_vfx_on_dt.setValue('Score VFX On')
        self.score_vfx_off_dt.setValue('Score VFX Off')


    def move_rbs(self):
        #left side
        self.music_on_rb.moveXY(-400, -150)
        self.music_off_rb.moveXY(-400, -30)
        self.bounce_vfx_on_rb.moveXY(-400, 90)
        #right side
        self.bounce_vfx_off_rb.moveXY(200, -150)
        self.score_vfx_on_rb.moveXY(200, -30)
        self.score_vfx_off_rb.moveXY(200, 90)

    def move_dt(self):
        #title
        self.title_text.moveXY(-80, 0)
        #left side
        self.music_on_dt.moveXY(-380, -165)
        self.music_off_dt.moveXY(-380, -45)
        self.bounce_vfx_on_dt.moveXY(-380, 75)
        #right side
        self.bounce_vfx_off_dt.moveXY(220, -165)
        self.score_vfx_on_dt.moveXY(220, -45)
        self.score_vfx_off_dt.moveXY(220, 75)


    def create_return_button(self):
        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return', fontSize=45, fontName= FONT_NAME)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                  WIN_H / 2 - self.return_button.getRect().height + 100)

    def enter_state(self, prev_state="settings"):
        self.return_state = prev_state
