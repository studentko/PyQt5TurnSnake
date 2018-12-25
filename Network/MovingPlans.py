from GameMechanic.Snake import *

class MovingPlans:
    def __init__(self):
        self.plans = {}

    def set_plan(self, snake, plan):
        self.plans[snake.indexInPlayer] = plan

    def get_plan(self, snake):
        return self.plans[snake.indexInPlayer]
