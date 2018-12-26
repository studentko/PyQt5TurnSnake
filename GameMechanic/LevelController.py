from GameMechanic.Snake import *
from GameMechanic.Player import *
from GameMechanic.WallBlock import *

class LevelController:
    def __init__(self, gameConfig):
        self.gameConfig = gameConfig
        self.gridContainer = GridContainer(15, 15)
        self.movables = []
        self.players = []
        # self.add_test_data()
        self.init_board()

    def add_test_data(self):
        snake = Snake(self.gridContainer, 3, 3, 5, 8, EMoveDirection.right)
        self.movables.append(snake)
        for _ in range(5):
            snake.moveSteps.append(EMoveDirection.down)

        for _ in range(10):
            snake.moveSteps.append(EMoveDirection.right)

    def init_board(self):
        self.init_walls()
        self.init_players()

    def init_walls(self):
        for i in range(self.gridContainer.width):
            self.gridContainer.move_block(WallBlock(), i, 0)
            self.gridContainer.move_block(WallBlock(), i, self.gridContainer.height - 1)
        for i in range(self.gridContainer.height - 2):
            self.gridContainer.move_block(WallBlock(), 0, i + 1)
            self.gridContainer.move_block(WallBlock(), self.gridContainer.width - 1, i + 1)

    def init_players(self):
        for i in range(self.gameConfig.playerNumber):
            player = Player()
            start_x = 0
            start_y = 0
            direction = EMoveDirection.none
            y_delta = 0
            if i == 0:
                start_x = 2
                start_y = 2
                direction = EMoveDirection.right
                y_delta = 2
            if i == 2:
                start_x = 2
                start_y = self.gridContainer.height - 3
                direction = EMoveDirection.right
                y_delta = -2
            if i == 1:
                start_x = self.gridContainer.width - 3
                start_y = self.gridContainer.height - 3
                direction = EMoveDirection.left
                y_delta = -2
            if i == 3:
                start_x = self.gridContainer.width - 3
                start_y = 2
                direction = EMoveDirection.left
                y_delta = 2

            for j in range(self.gameConfig.snakeNumber):
                snake = Snake(self.gridContainer, start_x, start_y, self.gameConfig.snakeSize + j,
                              self.gameConfig.snakeSteps, direction, EColor(i + 1))
                player.add_snake(snake)
                self.movables.append(snake)
                start_y = start_y + y_delta

            self.players.append(player)

    def make_turn_step(self):
        has_next = False
        for m in self.movables:
            has_next = m.make_step() or has_next
        self.collision_resolve()
        return has_next

    def has_turn_step(self):
        for m in self.movables:
            if m.has_steps():
                return True
        return False

    def collision_resolve(self):
        for x in self.gridContainer.blockMatrix:
            for cellset in x:
                if len(cellset) > 1:
                    walls = set()
                    snakeBlocks = set()
                    for block in cellset:
                        if isinstance(block, WallBlock):
                            walls.add(block)
                        if isinstance(block, SnakeBlock):
                            snakeBlocks.add(block)
                    if len(walls) > 0:
                        for sb in snakeBlocks:
                            sb.parentSnake.kill()

