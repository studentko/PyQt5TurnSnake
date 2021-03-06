from GameMechanic.Food import *
from GameMechanic.MovableObject import *
from multiprocessing import Process, Pipe
from enum import Enum


class FoodAsProcess(MovableObject):
    def __init__(self, gridContainer):
        super(FoodAsProcess, self).__init__()
        self.gridContainer = gridContainer
        self.food = Food(gridContainer)

        self.parent_conn = None
        self.child_conn = None
        self.process = None

    def start_process(self):
        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=FoodAsProcess.process_food,
                               args=(self.child_conn, self.gridContainer, self.food,))
        self.process.start()

    def send_process_command(self, command, data):
        self.parent_conn.send(command)
        self.parent_conn.send(data)

    @staticmethod
    def process_food(child_conn, gridContainer, foodArgs):
        food = foodArgs
        print("Started food process")

        while True:
            processCommand = child_conn.recv()
            print("Food process received command: ", processCommand)
            data = child_conn.recv()
            print("Food process received data: ", data);
            if processCommand == ProcessCommand.prepare_turn:
                x = food.block.x
                y = food.block.y
                food.gridContainer = gridContainer
                food.gridContainer.remove_blocks_at(food.block.x, food.block.y)
                food.block.x = -1
                food.block.y = -1
                food.gridContainer.move_block(food.block, x, y)
                food.prepare_turn()
            elif processCommand == ProcessCommand.make_step:
                food.make_step()
                child_conn.send([food.block.x, food.block.y])
            elif processCommand == ProcessCommand.has_steps:
                child_conn.send(food.has_steps())
            elif processCommand == ProcessCommand.kill:
                break

    def make_step(self):
        print("Making food step")
        if not self.has_steps():
            return False
        print("Making food step: sending make_step")
        self.send_process_command(ProcessCommand.make_step, None)
        cords = self.parent_conn.recv()
        print("koordinate: ", cords, " ;stare koord: ", self.food.block.x, ", ", self.food.block.y)
        self.gridContainer.move_block(self.food.block, cords[0], cords[1])
        print("food moved")
        return True

    def prepare_turn(self):
        self.send_process_command(ProcessCommand.prepare_turn, self.gridContainer)

    def has_steps(self):
        self.send_process_command(ProcessCommand.has_steps, None)
        has_steps = self.parent_conn.recv()
        return has_steps

    def kill(self):
        self.food.kill()
        self.send_process_command(ProcessCommand.kill, None)
        self.process.join(1)
        if self.process.exitcode is None:
            print("Terminating food process")
            self.process.terminate()

    def is_killed(self):
        return self.food.killed

class ProcessCommand(Enum):
    prepare_turn = 1
    make_step = 2
    has_steps = 3
    kill = 4
