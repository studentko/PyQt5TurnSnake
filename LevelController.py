from Snake import *


class LevelController:
    def __init__(self):
        self.gridContainer = GridContainer(15, 15)
        self.movables = []
        self.add_test_data()

    def add_test_data(self):
        snake = Snake(self.gridContainer, 3, 3, 5, 8, EMoveDirection.right)
        self.movables.append(snake)
        for _ in range(5):
            snake.moveSteps.append(EMoveDirection.down)

        for _ in range(10):
            snake.moveSteps.append(EMoveDirection.right)

    def make_turn_step(self):
        has_next = False
        for m in self.movables:
            has_next = m.make_step() or has_next
        return has_next

