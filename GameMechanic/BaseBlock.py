from enum import IntEnum


class BaseBlock:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.direction = 0
        self.drawable = EDrawable.Default

    def getDrawable(self):
        return self.drawable


class EDrawable(IntEnum):
    Default = -1
    Food1 = 0
    Head = 1
    Body = 2
    Tail = 3
    Wall = 4

