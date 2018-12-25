from enum import Enum


class MovableObject:
    def __init__(self):
        self.moveSteps = []

    def set_move_steps(self, moveSteps):
        self.moveSteps = []
        #self.moveSteps.append(moveSteps)
        self.moveSteps.extend(moveSteps)

    def get_move_steps(self):
        return self.moveSteps

    def make_step(self):
        pass

    def has_steps(self):
        return len(self.moveSteps) > 0


class EMoveDirection(Enum):
    none = (0, 0)
    up = (0, 1)
    right = (1, 0)
    down = (0, -1)
    left = (-1, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

