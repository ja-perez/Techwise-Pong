from typing import List, Dict
from src.commands.command import *
import pygame
import logging

logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

class InputHandler:
    def __init__(self):
        self.KeyboardCommands = dict()
        self.MouseCommands = dict()
        self.GamepadCommands = dict()

    def register_command(self, keycode: int, command: ICommand):
        self.KeyboardCommands.update({keycode: command})

    def handle_input(self) -> List[ICommand]:
        pygame.event.pump()

        #pressed = pygame.event.get(pygame.KEYDOWN)
        released = pygame.event.get(pygame.KEYUP)

        #mouse_pressed = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        #mouse_released = pygame.event.get(pygame.MOUSEBUTTONUP)
        #mouse_moved = pygame.event.get(pygame.MOUSEMOTION)
        #mouse_wheel = pygame.event.get(pygame.MOUSEWHEEL)

        for keycode, command in self.KeyboardCommands.items():
            if command.active == ActiveOn.RELEASED:
                for event in released:
                    if event.key == keycode:
                        command.execute(event.key)
        """
        for i, command in enumerate(self.MouseCommands):
            if command:
                if command.active == ActiveOn.RELEASED and released[i]:
                    command.execute()
        """
        #pygame.event.clear()
