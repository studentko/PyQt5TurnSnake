from .GridContainer import *
from .SnakeBlock import *

from GameMechanic.MovableObject import *
from GameMechanic.FoodBlock import EFoodType


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
        self.parentPlayer = None
        self.extend = 0

        for i in range(length):
            sb = SnakeBlock(self)
            sb.sbType = ESnakeBlockType.body
            sb.direction = moveDirection.getDirection()
            sb.headingDir = moveDirection
            sb.color = snakeColor
            gridContainer.move_block(sb, x + moveDirection.x * i, y + moveDirection.y * i)
            self.blocks.append(sb)
        self.blocks[0].sbType = ESnakeBlockType.tail
        self.blocks[-1].sbType = ESnakeBlockType.head

    def make_step(self):
        if len(self.moveSteps) <= 0 or self.lives <= 0:
            return False
        next_step = self.moveSteps.pop(0)

        tail = None
        if self.extend > 0:
            tail = SnakeBlock(self)
            tail.color = self.snakeColor
            self.extend = self.extend - 1
        else:
            tail = self.blocks.pop(0)

        head = self.blocks[-1]
        self.gridContainer.move_block(tail, head.x + next_step.x, head.y + next_step.y)
        tail.headingDir = next_step
        tail.direction = next_step.getDirection()
        tail.sbType = ESnakeBlockType.head


        #Snake block orientation code, clusterfuck written by trial and error, do not edit
        self.blocks[0].sbType = ESnakeBlockType.tail
        self.blocks[0].direction = self.blocks[1].headingDir.getDirection()

        if(self.blocks[-1].direction == tail.direction):
            head.sbType = ESnakeBlockType.body
        else:
            head.sbType = ESnakeBlockType.bodyAngle

            if(self.blocks[-1].direction == 0):
                if(next_step == EMoveDirection.left):
                    self.blocks[-1].direction = 180
                elif(next_step == EMoveDirection.right):
                    self.blocks[-1].direction = 90
            elif(self.blocks[-1].direction == 90):
                if(next_step == EMoveDirection.up):
                    self.blocks[-1].direction = 180
                elif(next_step == EMoveDirection.down):
                    self.blocks[-1].direction = 270
            elif (self.blocks[-1].direction == 180):
                if (next_step == EMoveDirection.right):
                    self.blocks[-1].direction = 0
                elif(next_step == EMoveDirection.left):
                    self.blocks[-1].direction = 270
            elif (self.blocks[-1].direction == 270):
                if (next_step == EMoveDirection.down):
                    self.blocks[-1].direction = 0
                elif(next_step == EMoveDirection.up):
                    self.blocks[-1].direction = 90

        self.blocks.append(tail)
        self.lastStepDirection = next_step
        return True

    def has_steps(self):
        return self.lives > 0 and super(Snake, self).has_steps()

    def get_head(self) -> SnakeBlock:
        return self.blocks[-1]

    def kill(self):
        for block in self.blocks:
            self.gridContainer.remove_block(block)
        self.lives = 0
        self.moveSteps = []
        self.parentPlayer.remove_snake(self)

    def eat_food(self, food):
        if food.foodType == EFoodType.step_extender:
            self.steps = self.steps + 1
        else:
            self.extend = self.extend + 1

