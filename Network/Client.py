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
