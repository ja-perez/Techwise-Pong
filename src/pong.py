from game import *

def main():
    pong = Game()
    while pong.running:
        pong.update()
    pong.teardown()
    
if __name__=="__main__":
    main()