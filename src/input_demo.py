from commands.command import *
from input.input_handler import *
import datetime
import pygame

def select(keycode=0):
    f = open("logfile.log", "a")
    f.write("{} : {} : {}\n".format(datetime.datetime.now(), "select()", chr(keycode)))
    f.close()


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("input_demo")

    s = SelectCommand(ActiveOn.PRESSED, select)
    ih = InputHandler()
    ih.register_command(pygame.K_ESCAPE, s)
    ih.register_command(pygame.K_EQUALS, s)
    clock = pygame.time.Clock()

    while True:
        CommandQueue = ih.handle_input()
        for command, args in CommandQueue:
            command.execute(args[0])

        if pygame.event.peek(pygame.QUIT):
            pygame.quit()

        clock.tick(60)


if __name__ == "__main__":
    main()
