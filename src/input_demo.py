from commands.command import *
from input.input_handler import *
import datetime
import pygame


def select(keycode):
    f = open("logfile.log", "a")
    f.write("{} : {} : {}\n".format(datetime.datetime.now(), "select()", chr(keycode)))
    f.close()

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("input_demo")

    s = SelectCommand(ActiveOn.RELEASED, select)
    ih = InputHandler()
    ih.register_command(pygame.K_ESCAPE, s)
    ih.register_command(pygame.K_EQUALS, s)
    clock = pygame.time.Clock()

    while True:
        ih.handle_input()
        if pygame.event.peek(pygame.QUIT):
            logging.shutdown()
            pygame.quit()

        clock.tick(60)


if __name__ == "__main__":
    main()