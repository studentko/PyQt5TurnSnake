from GameMechanic.MovableObject import *
from GameMechanic.FoodBlock import *
from random import *

class Food(MovableObject):
    def __init__(self, gridContainer):
        super(Food, self).__init__()
        self.gridContainer = gridContainer
        self.steps = randrange(1, 4)
        self.foodType = EFoodType(randrange(1, 3))
        self.block = FoodBlock(self.foodType, self)
        self.lastStepDirection = None

    def make_step(self):
        if len(self.moveSteps) <= 0:
            return False
        next_step = self.moveSteps.pop(0)
        self.gridContainer.move_block(self.block, self.block.x + next_step.x, self.block.y + next_step.y)
        self.lastStepDirection = next_step
        return True

    def prepare_turn(self):
        invalid = True
        trychoose = 0
        movedir = EMoveDirection.none
        while invalid and trychoose < 10:
            trychoose = trychoose + 1
            rmovedir = randrange(1, 5)
            if rmovedir == 1:
                movedir = EMoveDirection.down
            elif rmovedir == 2:
                movedir = EMoveDirection.up
            elif rmovedir == 3:
                movedir = EMoveDirection.right
            elif rmovedir == 4:
                movedir = EMoveDirection.left

            invalid = False
            for i in range(self.steps + 1):
                if self.gridContainer.has_blocks(self.block.x + (movedir.x * i), self.block.y + (movedir.y + i)):
                    invalid = True

        moves = []
        for i in range(self.steps):
            moves.append(movedir)
        self.set_move_steps(moves)

    def kill(self):
        self.gridContainer.remove_block(self.block)
