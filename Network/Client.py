import socket
import pickle
import base64
from Network.NetworkCommand import *
from Network.MovingPlans import *


class Client:
    def __init__(self, ip, port=12354):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def get_command(self) -> NetworkCommand:
        return get_command_from_socket(self.socket)

    def send_plans(self, movingPlans):
        send_command_to_socket(NetworkCommand(ENetworkCommand.call_for_plans, movingPlans), self.socket)

    def send_name(self, playerName):
        send_command_to_socket(NetworkCommand(ENetworkCommand.greeting, playerName), self.socket)

    @staticmethod
    def tournament_update_data_to_string(tud):
        matchTables = []
        current_tud = tud
        while current_tud is not None:
            mt = current_tud.matchTable.splitlines()
            matchTables.append(mt)
            current_tud = current_tud.previousTournamentData
        matchTables.reverse()

        allign = 22

        str_data = ""
        for i in range(len(matchTables)):
            str_data += ("Game " + str(i+1)).ljust(allign)
        str_data += "\n"

        next_add = True
        while next_add:
            next_add = False
            for mt in matchTables:
                name = ""
                if len(mt) > 0:
                    name = mt.pop(0)
                    next_add = True
                str_data += name.ljust(allign)
            str_data += "\n"

        str_data += "\n"
        if tud.tournamentCompleted:
            str_data += "Tournament winner: " + tud.tournamentWinner
        else:
            str_data += "Next game starting for 5 seconds..."

        return str_data
