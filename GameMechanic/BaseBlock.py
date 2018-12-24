from enum import Enum


class BaseBlock:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.drawable = EDrawable.Default
        self.direction = 0


class EDrawable(Enum):
    Default = 1
