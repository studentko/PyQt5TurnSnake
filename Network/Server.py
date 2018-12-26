import socket
import pickle
import sys
import base64
from .NetworkCommand import *
from Network.GridContainerUpdate import *
from GameMechanic.LevelController import *
from GameMechanic.GameConfig import *
from time import sleep


class Server:
    def __init__(self):
        self.ip = "0.0.0.0"
        self.port = 12355
        self.gameConfig = GameConfig()
        self.levelController = LevelController(self.gameConfig)
        self.socket = None
        self.clients = []

    def start_server(self):
        self.socket = socket.socket()
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.accept_clients()
        self.start_game_loop()

    def accept_clients(self):
        while len(self.clients) < self.gameConfig.playerNumber:
            c, addr = self.socket.accept()
            print('connection from ', addr)
            send_command_to_socket(NetworkCommand(ENetworkCommand.greeting, len(self.clients)), c)
            self.clients.append(c)

    def send_command(self, networkCommand):
        for c in self.clients:
            send_command_to_socket(networkCommand, c)

    def start_game_loop(self):
        self.send_command(NetworkCommand(ENetworkCommand.game_start, None))
        # self.send_command(NetworkCommand(ENetworkCommand.container_update, self.levelController.gridContainer))
        self.send_grid_update()

        while True:
            self.send_command(NetworkCommand(ENetworkCommand.turn_count_start, self.gameConfig.turnPlanTime))
            sleep(self.gameConfig.turnPlanTime)
            self.send_command(NetworkCommand(ENetworkCommand.call_for_plans, None))
            self.get_plans_from_clients()

            self.send_command(NetworkCommand(ENetworkCommand.update_start, None))
            while self.levelController.has_turn_step():
                self.levelController.make_turn_step()
                # self.send_command(NetworkCommand(ENetworkCommand.container_update, self.levelController.gridContainer))
                self.send_grid_update()
                sleep(0.2)
            self.send_command(NetworkCommand(ENetworkCommand.update_end, None))

    def send_grid_update(self):
        for i in range(len(self.clients)):
            c = self.clients[i]
            gcu = GridContainerUpdate(self.levelController.gridContainer,
                                      self.levelController.players[i].snakes)
            send_command_to_socket(NetworkCommand(ENetworkCommand.container_update, gcu), c)

    def get_plans_from_clients(self):
        for i in range(len(self.clients)):
            c = self.clients[i]
            command = get_command_from_socket(c)
            for snake in self.levelController.players[i].snakes:
                snake.set_move_steps(command.data.get_plan(snake))
