import pygwidgets
import pygame
from states.state import State
from Constants import *
from commands.command import *
from input.input_handler import *

class ThemesMenu(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.create_theme_rb()
        self.create_theme_dt()
        self.create_return_button()
        self.move_rbs()
        self.move_dt()
        self.return_state = ""
        self.theme_name = 'classic'

    def update(self):
        for event in pygame.event.get():

            if self.classic_rb.handleEvent(event):
                self.game.states["local"].classic_bool = True
                self.game.states["local"].themes.classic()
                self.game.states["local"].update_theme()

            if self.cyberpunk_rb.handleEvent(event):
                self.game.states["local"].classic_bool = False
                self.game.states["local"].themes.cyberpunk()
                self.game.states["local"].update_theme()

            if self.disco_rb.handleEvent(event):
                self.game.states["local"].classic_bool = False
                self.game.states["local"].themes.disco()
                self.game.states["local"].update_theme()
            if self.science_rb.handleEvent(event):
                self.game.states["local"].classic_bool = False
                self.game.states["local"].themes.science()
                self.game.states["local"].update_theme()

            if self.snow_rb.handleEvent(event):
                self.game.states["local"].classic_bool = False
                self.game.states["local"].themes.snow()
                self.game.states["local"].update_theme()

            if self.western_rb.handleEvent(event):
                self.game.states["local"].classic_bool = False
                self.game.states["local"].themes.western()
                self.game.states["local"].update_theme()

            if self.return_button.handleEvent(event):
                self.change_state(self.return_state)

    def render(self):
        self.button_display()
        #self.title_text()


    # def title_text(self):
    #     font = pygame.font.Font(FONT_NAME, 50)
    #     text_surface = font.render("THEMES", True, BLACK)
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (GAME_W, GAME_H//2 - 80)
    #     self.game.screen.blit(text_surface, text_rect)


    def button_display(self):
        #RADIO BUTTONS
        self.classic_rb.draw()
        self.cyberpunk_rb.draw()
        self.disco_rb.draw()
        self.science_rb.draw()
        self.snow_rb.draw()
        self.western_rb.draw()
        #DISPLAY BUTTONS
        self.title_text.draw()
        self.classic_dt.draw()
        self.cyberpunk_dt.draw()
        self.disco_dt.draw()
        self.science_dt.draw()
        self.snow_dt.draw()
        self.western_dt.draw()

        #RETURN BUTTON
        self.return_button.draw()

    def create_theme_rb(self):
        height_var = 50
        width_var = 50
        font_size = 1
        self.classic_rb = pygwidgets.TextRadioButton(window=self.game.screen,
                                                     loc=(GAME_W, GAME_H),
                                                     group='ThemeRadioButton',
                                                     text='Classic',
                                                     fontName=FONT_NAME,
                                                     fontSize=font_size)
        self.cyberpunk_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                       'ThemeRadioButton',
                                                       text='Cyberpunk',
                                                       fontName='neon_font.ttf',
                                                       fontSize=font_size)
        self.disco_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                   'ThemeRadioButton',
                                                   text='Disco',
                                                   fontName=FONT_NAME,
                                                   fontSize=font_size)
        self.science_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                     'ThemeRadioButton',
                                                     text='Science',
                                                     fontName=FONT_NAME,
                                                     fontSize=font_size)
        self.snow_rb = pygwidgets.TextRadioButton(self.game.screen, (GAME_W, GAME_H),
                                                  'ThemeRadioButton',
                                                  text='Snow',
                                                  fontName=FONT_NAME,
                                                  fontSize=font_size)
        self.western_rb = pygwidgets.TextRadioButton(self.game.screen,(GAME_W, GAME_H),
                                                     'ThemeRadioButton',
                                                     text='Western',
                                                     fontName=FONT_NAME,
                                                     fontSize=font_size)
    def create_theme_dt(self):
        self.title_text = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H//2 - 80),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)

        self.classic_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.cyberpunk_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.disco_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)



        self.science_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.snow_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)


        self.western_dt = pygwidgets.DisplayText(self.game.screen, (GAME_W, GAME_H),
                                                   fontName=FONT_NAME,
                                                   fontSize=50,
                                                   textColor=CYBERPUNK_1)

        self.title_text.setText("Themes Menu")
        self.classic_dt.setValue('Classic')
        self.cyberpunk_dt.setValue('CyberPunk')
        self.disco_dt.setValue('Disco')
        self.science_dt.setValue('Science')
        self.snow_dt.setValue('Snow')
        self.western_dt.setValue('Western')


    def move_rbs(self):
        #left side
        self.classic_rb.moveXY(-400, -150)
        self.cyberpunk_rb.moveXY(-400, -30)
        self.disco_rb.moveXY(-400, 90)
        #right side
        self.science_rb.moveXY(200, -150)
        self.snow_rb.moveXY(200, -30)
        self.western_rb.moveXY(200, 90)

    def move_dt(self):
        #title
        self.title_text.moveXY(-90, 0)
        #left side
        self.classic_dt.moveXY(-380, -165)
        self.cyberpunk_dt.moveXY(-380, -45)
        self.disco_dt.moveXY(-380, 75)
        #right side
        self.science_dt.moveXY(220, -165)
        self.snow_dt.moveXY(220, -45)
        self.western_dt.moveXY(220, 75)


    def create_return_button(self):
        self.return_button = pygwidgets.TextButton(self.game.screen, (0, 0), 'Return', fontSize=45, fontName= FONT_NAME)
        self.return_button.moveXY(WIN_W / 2 - self.return_button.getRect().width / 2,
                                  WIN_H / 2 - self.return_button.getRect().height + 100)

    def enter_state(self, prev_state="graphicsmenu"):
        self.return_state = prev_state
