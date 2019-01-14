from .NetworkCommand import *
from Network.GridContainerUpdate import *
from Network.GreetingData import *
from Network.GameEndData import *
from GameMechanic.LevelController import *
from GameMechanic.GameConfig import *
from time import sleep
from threading import Thread

class ServerGame:
    def __init__(self, gameConfig, clients, server):
        self.gameConfig = gameConfig
        self.clients = clients
        self.server = server
        self.levelController = LevelController(gameConfig)
        self.winner = -1

    def send_command(self, networkCommand):
        threads = []
        for c in self.clients:
            t = send_command_to_socket_threaded(networkCommand, c)
            threads.append(t)
        for t in threads:
            t.join()

    def start_game_loop(self):
        if self.server.tournamentUpdateData is not None:
            self.send_command(NetworkCommand(ENetworkCommand.tournament_update, self.server.tournamentUpdateData))
            sleep(5)

        self.send_command(NetworkCommand(ENetworkCommand.game_start, None))
        # self.send_command(NetworkCommand(ENetworkCommand.container_update, self.levelController.gridContainer))
        self.send_grid_update()

        while True:
            self.send_command(NetworkCommand(ENetworkCommand.turn_count_start, self.gameConfig.turnPlanTime))
            sleep(self.gameConfig.turnPlanTime)
            self.send_command(NetworkCommand(ENetworkCommand.call_for_plans, None))
            self.get_plans_from_clients()

            self.send_command(NetworkCommand(ENetworkCommand.update_start, None))
            self.levelController.prepare_turn()
            while self.levelController.has_turn_step():
                self.levelController.make_turn_step()
                self.send_grid_update()
                sleep(0.2)
            if self.levelController.complete_turn():
                self.send_grid_update()
            self.send_command(NetworkCommand(ENetworkCommand.update_end, None))

            winner = self.levelController.who_is_winner()
            if winner > -1:
                gameEndData = GameEndData(winner)
                gameEndData.has_next_game = self.gameConfig.tournament
                self.send_command(NetworkCommand(ENetworkCommand.game_end, gameEndData))
                self.winner = winner
                break

    def send_grid_update(self):
        threads = []
        for i in range(len(self.clients)):
            c = self.clients[i]
            gcu = GridContainerUpdate(self.levelController.gridContainer,
                                      self.levelController.players[i].snakes)
            t = send_command_to_socket_threaded(NetworkCommand(ENetworkCommand.container_update, gcu), c)
            threads.append(t)
        for t in threads:
            t.join()

    def get_plans_from_clients(self):
        for i in range(len(self.clients)):
            c = self.clients[i]
            command = get_command_from_socket(c)
            for snake in self.levelController.players[i].snakes:
                snake.set_move_steps(command.data.get_plan(snake))

    def get_winner_client(self):
        return self.clients[self.winner]
