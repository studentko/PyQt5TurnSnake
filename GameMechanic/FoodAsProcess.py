from GameMechanic.Food import *
from GameMechanic.MovableObject import *
from multiprocessing import Process, Pipe
from enum import Enum


class FoodAsProcess(MovableObject):
    def __init__(self, gridContainer):
        super(FoodAsProcess, self).__init__()
        self.gridContainer = gridContainer
        self.food = Food(gridContainer)


        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=FoodAsProcess.process_food, args=(self.child_conn, self.gridContainer, self.food))

    def send_process_command(self, command, data):
        self.parent_conn.send(command)
        self.parent_conn.send(data)

    @staticmethod
    def process_food(child_conn, gridContainer, foodArgs):
        food = foodArgs

        while True:
            processCommand = child_conn.recv()
            data = child_conn.recv()
            if processCommand == ProcessCommand.prepare_turn:
                food.gridContainer = gridContainer
                food.gridContainer.remove_blocks_at(food.block.x, food.block.y)
                x = food.block.x
                y = food.block.y
                food.block.x = -1
                food.block.y = -1
                food.gridContainer.move_block(x, y)
            elif processCommand == ProcessCommand.make_step:
                food.make_step()
                child_conn.send([food.block.x, food.block.y])
            elif processCommand == ProcessCommand.has_steps:
                child_conn.send(food.has_steps())
            elif processCommand == ProcessCommand.kill:
                break

    def make_step(self):
        if not self.has_steps():
            return False
        self.send_process_command(ProcessCommand.make_step, None)
        cords = self.parent_conn.recv()
        self.gridContainer.move_block(self.food, cords[0], cords[1])
        return True

    def prepare_turn(self):
        self.send_process_command(ProcessCommand.prepare_turn, self.gridContainer)

    def has_steps(self):
        self.send_process_command(ProcessCommand.has_steps, None)
        has_steps = self.parent_conn.recv()
        return has_steps

    def kill(self):
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
