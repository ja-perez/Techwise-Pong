from typing import List, Dict
from commands.command import *
import functools
import pygame


class InputHandler:
    def __init__(self):
        self.KeyboardCommands = dict()
        self.MouseCommands = dict()
        self.GamepadCommands = dict()
        self.MouseButtons = {"lclick": 1, "mclick": 2, "rclick": 3, "scrolldown": 4, "scrollup": 5}
    def register_command(self, keycode: int, command: ICommand):
        self.KeyboardCommands.update({keycode: command})

    def register_ms_command(self, button: str, command: ICommand):
        if button in self.MouseButtons:
            keycode = self.MouseButtons[button]
            self.MouseCommands.update({keycode: command})

    def handle_input(self) -> List[ICommand]:
        CommandQueue = list()
        pygame.event.pump()

        key_pressed = pygame.event.get(pygame.KEYDOWN)
        key_released = pygame.event.get(pygame.KEYUP)
        mouse_pressed = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        mouse_released = pygame.event.get(pygame.MOUSEBUTTONUP)
        # mouse_moved = pygame.event.get(pygame.MOUSEMOTION)
        # mouse_wheel = pygame.event.get(pygame.MOUSEWHEEL)
        # functools here seems like a great choice, but would like to keep the queue
        # strictly commands and not callables to ensure we can maintain talking about
        # a command in a wholly fashion. potentially a tuple with a command and a list of
        # their arguments, or a tuple of a command and a partialed callable?

        for keycode, command in self.KeyboardCommands.items():
            if command.active == ActiveOn.PRESSED or command.active == ActiveOn.BOTH:
                for event in key_pressed:
                    if event.key == keycode:
                        # CommandQueue.append((command, functools.partial(command.execute, keycode)))
                        CommandQueue.append((command, [keycode]))
            if command.active == ActiveOn.RELEASED or command.active == ActiveOn.BOTH:
                for event in key_released:
                    if event.key == keycode:
                        # CommandQueue.append(functools.partial(command.execute, keycode))
                        CommandQueue.append((command, [keycode]))

        for keycode, command in self.MouseCommands.items():
            if command.active == ActiveOn.PRESSED or command.active == ActiveOn.BOTH:
                for event in mouse_pressed:
                    if event.button == keycode:
                        CommandQueue.append((command, [keycode]))
            if command.active == ActiveOn.RELEASED or command.active == ActiveOn.BOTH:
                for event in mouse_released:
                    if event.button == keycode:
                        CommandQueue.append((command, [keycode]))
        return CommandQueue

        """
        for i, command in enumerate(self.MouseCommands):
            if command:
                if command.active == ActiveOn.RELEASED and released[i]:
                    command.execute()
        """
        # pygame.event.clear()
