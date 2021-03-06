from enum import Enum
import pickle
import base64
import sys
import socket
from time import sleep
from threading import Thread

class ENetworkCommand(Enum):
    socket_failed = -1
    greeting = 1
    game_start = 2
    container_update = 3
    turn_count_start = 4
    call_for_plans = 5
    update_start = 6
    update_end = 7
    game_end = 8
    tournament_update = 9
    server_closing = 10


class NetworkCommand:
    def __init__(self, comm, data):
        self.comm = comm
        self.data = data


def send_command_to_socket_threaded(networkCommand, socket):
    t = Thread(target=send_command_to_socket, args=(networkCommand, socket))
    t.start()
    return t;


def send_command_to_socket(networkCommand, socket):
        pickled = pickle.dumps(networkCommand)
        pickled = base64.encodebytes(pickled)
        pickled = pickled
        size = len(pickled)
        bytes_size = size.to_bytes(4, byteorder='little')
        bytes_size = bytes_size
        # bytes_size = base64.encodebytes(size)
        print("sending: ", networkCommand.comm, " | size: ", bytes_size)
        try:
            send_data(socket, bytes_size, 4)
            sleep(0.1)
            send_data(socket, pickled, size)
        except IOError:
            print("Unable to send command: " + networkCommand.comm)


def get_command_from_socket(sock):
        try:
            size_bytes = receive_data(sock, 4)
            size = int.from_bytes(size_bytes, byteorder='little')
            # size = 8192
            base64comm = receive_data(sock, size)
            networkCommand = pickle.loads(base64.decodebytes(base64comm))
            print("received: ", networkCommand.comm, " | size: ", size_bytes)
            return networkCommand
        except IOError:
            print("Unable to receive command")
            return NetworkCommand(ENetworkCommand.socket_failed, None)


def receive_data(sock, datalen):
    chunks = []
    bytes_recd = 0
    while bytes_recd < datalen:
        chunk = sock.recv(min(datalen - bytes_recd, 2048))
        if chunk == b'':
            raise IOError("socket connection broken")
            print("noting received; left to receive: ", datalen - bytes_recd)
            sleep(0.2)
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)


def send_data(sock, msg, datalen):
        totalsent = 0
        while totalsent < datalen:
            print("sending data of len: ", len(msg[totalsent:]))
            sent = sock.send(msg[totalsent:])
            if sent == 0:
                raise IOError("socket connection broken")
                print("noting sent; left to sent: ", datalen - totalsent)
                sleep(0.2)
            totalsent = totalsent + sent
