from GameMechanic.Snake import *
from GameMechanic.Player import *
from GameMechanic.WallBlock import *
from GameMechanic.Food import *
from GameMechanic.FoodAsProcess import *
from GameMechanic.DeusBlock import *
from random import randrange

class LevelController:
    def __init__(self, gameConfig):
        self.gameConfig = gameConfig
        self.gridContainer = GridContainer(15, 15)
        self.movables = []
        self.players = []
        # self.add_test_data()
        self.init_board()
        self.foods = []
        self.foodSpawnTurn = randrange(1, 2)
        self.foodblockprocessbind = dict()
        self.deus = None
        self.deusSpawnTurn = randrange(2, 3)

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
        playerNumber = self.gameConfig.playerNumber
        if self.gameConfig.tournament:
            playerNumber = 2
        for i in range(playerNumber):
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

    def prepare_turn(self):
        if self.deus is not None:
            self.deus.prepare_turn(self)
        for food in self.foods:
                food.prepare_turn()
        for player in self.players:
            for snake in player.snakes:
                snake.prepare_turn()
    def make_turn_step(self):
        has_next = False
        for m in self.movables:
            has_next = m.make_step() or has_next
        self.collision_resolve()
        return has_next

    def complete_turn(self):
        created = False

        self.deusSpawnTurn -= 1
        if self.deusSpawnTurn <= 0:
            self.deusSpawnTurn = randrange(4, 6)
            tries = 0
            while tries < 10:
                tries += 1
                x = randrange(0, self.gridContainer.width + 1)
                y = randrange(0, self.gridContainer.height + 1)
                if not self.gridContainer.has_blocks(x, y):
                    self.deus = DeusBlock()
                    self.gridContainer.move_block(self.deus, x, y)
                    break

        self.foodSpawnTurn = self.foodSpawnTurn - 1
        if self.foodSpawnTurn <= 0:
            self.foodSpawnTurn = randrange(1, 2)
            tries = 0
            while ++tries < 10:
                tries += 1
                x = randrange(0, self.gridContainer.width + 1)
                y = randrange(0, self.gridContainer.height + 1)
                if not self.gridContainer.has_blocks(x, y):
                    food = FoodAsProcess(self.gridContainer)
                    self.gridContainer.move_block(food.food.block, x, y)
                    self.movables.append(food)
                    self.foods.append(food)
                    self.foodblockprocessbind[food.food.block] = food

                    food.start_process()
                    return True

        return created

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
                    foodBlocks = set()
                    deusBlock = None
                    for block in cellset:
                        if isinstance(block, WallBlock):
                            walls.add(block)
                        if isinstance(block, SnakeBlock):
                            snakeBlocks.add(block)
                        if isinstance(block, FoodBlock):
                            foodBlocks.add(block)
                        if isinstance(block, DeusBlock):
                            deusBlock = block
                    if len(walls) > 0:
                        for sb in snakeBlocks:
                            sb.parentSnake.kill()
                    elif len(snakeBlocks) >= 2:
                        for sb in snakeBlocks:
                            if (sb.sbType == ESnakeBlockType.head):
                                sb.parentSnake.kill()
                    elif len(foodBlocks) > 0 and len(snakeBlocks) == 1:
                        sb = snakeBlocks.pop()
                        if sb.sbType == ESnakeBlockType.head:
                            snake = sb.parentSnake
                            for fb in foodBlocks:
                                snake.eat_food(fb.parent)

                    if deusBlock is not None and len(snakeBlocks) == 1:
                        snake = snakeBlocks.pop().parentSnake
                        self.apply_deus(snake)

                    for fb in foodBlocks:
                        parent = self.foodblockprocessbind[fb]
                        self.movables.remove(parent)
                        self.foods.remove(parent)
                        parent.kill()

    def apply_deus(self, snake):
        if self.deus is None or self.deus.drawable == EDrawable.DeusActivating:
            print("Deus is not ready yet")
            return
        if self.deus.gift:
            print("Deus will give you gift")
            for p in self.players:
                if snake.parentPlayer != p:
                    if len(p.snakes) > 0:
                        s = p.snakes[0]
                        s.kill()
        else:
            print("You got punish from deus")
            snake.kill()
        self.gridContainer.remove_block(self.deus)
        self.deus = None

    def who_is_winner(self):
        active_players = 0
        winner_index = -1
        for p in self.players:
            if len(p.snakes) > 0:
                active_players += + 1
            winner_index += 1
        if active_players == 1:
            for i in range(len(self.players)):
                if len(self.players[i].snakes) > 0:
                    return i
        if active_players == 0:
            return 0
        return -1

    def complete_level(self):
        for food in self.foods:
            food.kill()
