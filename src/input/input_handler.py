from typing import List, Dict
from commands.command import *
import functools
import pygame

class InputHandler:
    def __init__(self):
        self.KeyboardCommands = dict()
        self.MouseCommands = dict()
        self.GamepadCommands = dict()

    def register_command(self, keycode: int, command: ICommand):
        self.KeyboardCommands.update({keycode:command})

    def handle_input(self) -> List[ICommand]:
        CommandQueue = list()
        pygame.event.pump()

        pressed = pygame.event.get(pygame.KEYDOWN)
        released = pygame.event.get(pygame.KEYUP)
        # mouse_pressed = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        # mouse_released = pygame.event.get(pygame.MOUSEBUTTONUP)
        # mouse_moved = pygame.event.get(pygame.MOUSEMOTION)
        # mouse_wheel = pygame.event.get(pygame.MOUSEWHEEL)

        #functools here seems like a great choice, but would like to keep the queue
        #strictly commands and not callables to ensure we can maintain talking about
        #a command in a wholly fashion. potentially a tuple with a command and a list of
        #their arguments, or a tuple of a command and a partialed callable?
        if pressed or released:
            print(pressed, '\t', released, '\t', self.KeyboardCommands.items())

        for keycode, command in self.KeyboardCommands.items():
            if command.active == ActiveOn.PRESSED:
                for event in pressed:
                    if event.key == keycode:
                        #CommandQueue.append((command, functools.partial(command.execute, keycode)))
                        CommandQueue.append((command, [keycode]))
            if command.active == ActiveOn.RELEASED:
                for event in released:
                    if event.key == keycode:
                        #CommandQueue.append(functools.partial(command.execute, keycode))
                        CommandQueue.append((command, [keycode]))
        return CommandQueue
        """
        for i, command in enumerate(self.MouseCommands):
            if command:
                if command.active == ActiveOn.RELEASED and released[i]:
                    command.execute()
        """
        # pygame.event.clear()
