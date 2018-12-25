from GameMechanic.Snake import *


class Player:
    def __init__(self):
        self.snakes = []

    def add_snake(self, snake):
        snake.indexInPlayer = len(self.snakes)
        self.snakes.append(snake)
