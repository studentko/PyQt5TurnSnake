from enum import *


class BaseBlock:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.direction = 0
        self.drawable = EDrawable.Default
        self.color = EColor.none

    def getDrawable(self):
        return self.drawable

    def get_color(self):
        return self.color

class EDrawable(IntEnum):
    Default = -1
    Food1 = 0
    Head = 1
    Body = 2
    Tail = 3
    Wall = 4

class EColor(IntEnum):
    none = 0
    red = 1
    blue = 2
    yellow = 3
    purple = 4
