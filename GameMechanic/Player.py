from GameMechanic.Snake import *


class Player:
    def __init__(self):
        self.snakes = []

    def add_snake(self, snake):
        snake.indexInPlayer = len(self.snakes)
        self.snakes.append(snake)

    def get_alive_snakes(self):
        alive_snakes = []
        for snake in self.snakes:
            if snake.lives > 0:
                alive_snakes.append(snake)
        return alive_snakes
