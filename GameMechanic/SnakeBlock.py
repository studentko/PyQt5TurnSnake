from enum import IntEnum

from GameMechanic.BaseBlock import BaseBlock, EDrawable


class SnakeBlock(BaseBlock):
    def __init__(self):
        super(SnakeBlock, self).__init__()
        self.sbType = ESnakeBlockType.none
    

    def getDrawable(self):
        return EDrawable(int(self.sbType))


class ESnakeBlockType(IntEnum):
    none = 0
    head = 1
    body = 2
    tail = 3

