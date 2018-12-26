from .GridContainer import *
from .SnakeBlock import *

from GameMechanic.MovableObject import *


class Snake(MovableObject):
    def __init__(self, gridContainer, x, y, length, steps, moveDirection, snakeColor):
        super(Snake, self).__init__()
        self.gridContainer = gridContainer
        self.steps = steps
        self.blocks = []
        self.indexInPlayer = -1
        self.lastStepDirection = moveDirection
        self.snakeColor = snakeColor
        self.lives = 1

        for i in range(length):
            sb = SnakeBlock(self)
            sb.sbType = ESnakeBlockType.body
            sb.direction = moveDirection.getDirection()
            sb.color = snakeColor
            gridContainer.move_block(sb, x + moveDirection.x * i, y + moveDirection.y * i)
            self.blocks.append(sb)
        self.blocks[0].sbType = ESnakeBlockType.tail
        self.blocks[-1].sbType = ESnakeBlockType.head

    def make_step(self):
        if len(self.moveSteps) <= 0 or self.lives <= 0:
            return False
        next_step = self.moveSteps.pop(0)
        tail = self.blocks.pop(0)
        head = self.blocks[-1]
        self.gridContainer.move_block(tail, head.x + next_step.x, head.y + next_step.y)
        tail.direction = next_step.getDirection()
        tail.sbType = ESnakeBlockType.head
        head.sbType = ESnakeBlockType.body
        self.blocks.append(tail)
        self.lastStepDirection = next_step
        return True

    def has_steps(self):
        return self.lives > 0 and super().has_steps()

    def get_head(self):
        return self.blocks[-1]

    def kill(self):
        for block in self.blocks:
            self.gridContainer.remove_block(block)
        self.lives = 0
        self.moveSteps = []
