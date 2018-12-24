from enum import Enum

from GameMechanic.BaseBlock import BaseBlock


class SnakeBlock(BaseBlock):
    def __init__(self):
        super(SnakeBlock, self).__init__()
        self.sbType = ESnakeBlockType.none


class ESnakeBlockType(Enum):
    none = 0
    head = 1
    body = 2
    tail = 3

