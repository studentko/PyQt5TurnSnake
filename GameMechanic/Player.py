from GameMechanic.Snake import *


class Player:
    def __init__(self):
        self.snakes = []

    def add_snake(self, snake):
        snake.indexInPlayer = len(self.snakes)
        snake.parentPlayer = self
        self.snakes.append(snake)

    def remove_snake(self, snake):
        self.snakes.remove(snake)
        for i in range(len(self.snakes)):
            self.snakes[i].indexInPlayer = i

    def get_alive_snakes(self):
        alive_snakes = []
        for snake in self.snakes:
            if snake.lives > 0:
                alive_snakes.append(snake)
        return alive_snakes
