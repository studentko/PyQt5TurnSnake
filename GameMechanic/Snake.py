from .GridContainer import *
from .SnakeBlock import *

from GameMechanic.MovableObject import *


class Snake(MovableObject):
    def __init__(self, gridContainer, x, y, length, steps, moveDirection):
        super(Snake, self).__init__()
        self.gridContainer = gridContainer
        self.steps = steps
        self.blocks = []
        self.indexInPlayer = -1
        self.lastStepDirection = moveDirection

        for i in range(length):
            sb = SnakeBlock()
            sb.sbType = ESnakeBlockType.body
            gridContainer.move_block(sb, x + moveDirection.x * i, y + moveDirection.y * i)
            self.blocks.append(sb)
        self.blocks[0].sbType = ESnakeBlockType.tail
        self.blocks[-1].sbType = ESnakeBlockType.head

    def make_step(self):
        if len(self.moveSteps) <= 0:
            return False
        next_step = self.moveSteps.pop(0)
        tail = self.blocks.pop(0)
        head = self.blocks[-1]
        self.gridContainer.move_block(tail, head.x + next_step.x, head.y + next_step.y)
        tail.sbType = ESnakeBlockType.head
        head.sbType = ESnakeBlockType.body
        self.blocks.append(tail)
        self.lastStepDirection = next_step
        return True

    def get_head(self):
        return self.blocks[-1]
