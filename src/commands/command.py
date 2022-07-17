from abc import abstractstaticmethod
from enum import Enum, unique
from typing import Callable
#from globals import States
#s = States["MainMenu"]
@unique
class ActiveOn(Enum):
    PRESSED = 1
    RELEASED = 2

class ICommand:
    def __init__(self, active: ActiveOn, function: Callable):
        self.active = active
        self.function = function
        self.delay = 0

    @abstractstaticmethod
    def execute(game: Game):
        """"""
    @abstractstaticmethod
    def undo():
        """"""

class SelectCommand(ICommand):
    def __init__(self, active: ActiveOn, function: Callable):
        super(SelectCommand, self).__init__(active, function)
        
    def execute(self, keycode):

        self.function(keycode)

    def undo(self):
        pass

class ScrollUpCommand(ICommand):
    pass

class ScrollDownCommand(ICommand):
    pass
