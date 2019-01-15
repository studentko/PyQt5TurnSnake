import socket
import pickle
import sys
import base64
from .NetworkCommand import *
from Network.GridContainerUpdate import *
from Network.GreetingData import *
from Network.GameEndData import *
from GameMechanic.LevelController import *
from GameMechanic.GameConfig import *
from time import sleep
from Network.ServerGame import ServerGame
from Network.TournamentUpdateData import TournamentUpdateData
from threading import Thread

class Server:
    def __init__(self, gameConfig, port=12355, ip="0.0.0.0"):
        self.ip = ip
        self.port = port
        self.gameConfig = gameConfig
        self.levelController = LevelController(self.gameConfig)
        self.socket = None
        self.clients = []
        self.clientsNames = dict()
        self.serverGames = []
        self.tournamentUpdateData = None
        self.gameNumber = 1

    def start_server(self):
        self.socket = socket.socket()
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.accept_clients()
        self.create_server_games()
        self.start_game_loop()
        self.close_server()

    def send_command(self, networkCommand):
        threads = []
        for c in self.clients:
            t = send_command_to_socket_threaded(networkCommand, c)
            threads.append(t)
        for t in threads:
            t.join()

    def accept_clients(self):
        while len(self.clients) < self.gameConfig.playerNumber:
            c, addr = self.socket.accept()
            print('connection from ', addr)
            greetingData = GreetingData(len(self.clients), self.levelController.gridContainer.width,
                                        self.levelController.gridContainer.height)
            send_command_to_socket(NetworkCommand(ENetworkCommand.greeting, greetingData), c)

            command = get_command_from_socket(c)
            if command.data is None or command.comm == ENetworkCommand.socket_failed:
                self.clientsNames[c] = "Player " + str(len(self.clients) + 1)
            else:
                self.clientsNames[c] = command.data

            self.clients.append(c)

    def create_server_games(self):
        winner_client = None
        if self.gameConfig.tournament:
            clients = []
            if len(self.serverGames) > 0:
                for game in self.serverGames:
                    clients.append(game.get_winner_client())
            else:
                clients.extend(self.clients)
                shuffle(clients)

            self.serverGames.clear()
            clients_for_game = []
            for client in clients:
                clients_for_game.append(client)
                if len(clients_for_game) >= 2:
                    serverGame = ServerGame(self.gameConfig, clients_for_game, self)
                    self.serverGames.append(serverGame)
                    clients_for_game = []

            if len(clients_for_game) >= 1:
                serverGame = ServerGame(self.gameConfig, clients_for_game, self)
                self.serverGames.append(serverGame)

            if len(clients) == 1:
                winner_client = clients[0]
                self.serverGames.clear()
        else:
            self.serverGames.clear()
            serverGame = ServerGame(self.gameConfig, self.clients, self)
            self.serverGames.append(serverGame)

        if self.gameConfig.tournament:
            tud = TournamentUpdateData()
            tud.previousTournamentData = self.tournamentUpdateData
            tud.gameNumber = self.gameNumber
            self.gameNumber += 1

            tud.matchTable = ""
            if winner_client is None:
                for game in self.serverGames:
                    line = ""
                    for client in game.clients:
                        if len(line) > 0:
                            line += " vs "
                        line += self.clientsNames[client]
                    tud.matchTable += line + "\n"
            else:
                tud.matchTable = self.clientsNames[winner_client]
                tud.tournamentCompleted = True
                tud.tournamentWinner = self.clientsNames[winner_client]

            self.tournamentUpdateData = tud

    def start_game_loop(self):
        while True:
            threads = []
            for game in self.serverGames:
                t = Thread(target=game.start_game_loop)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            if self.gameConfig.tournament is False:
                break

            if len(self.serverGames) > 0:
                self.create_server_games()
            else:
                self.send_command(NetworkCommand(ENetworkCommand.tournament_update, self.tournamentUpdateData))
                break

    def close_server(self):
        self.send_command(NetworkCommand(ENetworkCommand.server_closing, None))
        for c in self.clients:
            c.close()
        self.socket.close()
        print("-----------------------------> Server completed")
