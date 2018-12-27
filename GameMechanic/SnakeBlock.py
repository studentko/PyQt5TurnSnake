from enum import IntEnum

from GameMechanic.BaseBlock import BaseBlock, EDrawable


class SnakeBlock(BaseBlock):
    def __init__(self, parentSnake):
        super(SnakeBlock, self).__init__()
        self.sbType = ESnakeBlockType.none
        self.parentSnake = parentSnake
        #actual part direction, baseblock.direction used for texture direction
        self.headingDir = 0

    def getDrawable(self):
        return EDrawable(int(self.sbType - 1))


class ESnakeBlockType(IntEnum):
    none = 0
    head = 1
    body = 2
    tail = 3
    bodyAngle = 4

