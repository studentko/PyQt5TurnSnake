from GameMechanic.BaseBlock import *


class FoodBlock(BaseBlock):
    def __init__(self, foodType):
        super(FoodBlock, self).__init__()
        self.foodType = foodType
        if foodType == EFoodType.step_extender:
            self.drawable = EDrawable.FoodStep
        else:
            self.drawable = EDrawable.FoodSnake


class EFoodType(Enum):
    step_extender = 1
    snake_extender = 2