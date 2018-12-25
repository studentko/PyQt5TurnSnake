from enum import Enum
import pickle
import base64
import sys
import socket
from time import sleep

class ENetworkCommand(Enum):
    greeting = 1
    game_start = 2
    container_update = 3
    turn_count_start = 4
    call_for_plans = 5
    update_start = 6
    update_end = 7


class NetworkCommand:
    def __init__(self, comm, data):
        self.comm = comm
        self.data = data


def send_command_to_socket(networkCommand, socket):
        pickled = pickle.dumps(networkCommand)
        pickled = base64.encodebytes(pickled)
        pickled = pickled
        size = len(pickled)
        bytes_size = size.to_bytes(4, byteorder='little')
        bytes_size = bytes_size
        # bytes_size = base64.encodebytes(size)
        print("pickle size: ", size, "|", bytes_size)
        send_data(socket, bytes_size, 4)
        sleep(0.1)
        send_data(socket, pickled, size)

def get_command_from_socket(sock):
        size_bytes = receive_data(sock, 4)
        size = int.from_bytes(size_bytes, byteorder='little')
        # size = 8192
        print("pickle size to get: ", size, "|", size_bytes)
        base64comm = receive_data(sock, size)
        print("================ PRIMIO: ", len(base64comm))
        networkCommand = pickle.loads(base64.decodebytes(base64comm))
        return networkCommand

def receive_data(sock, datalen):
    chunks = []
    bytes_recd = 0
    while bytes_recd < datalen:
        chunk = sock.recv(min(datalen - bytes_recd, 2048))
        if chunk == b'':
            # raise RuntimeError("socket connection broken")
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
                # raise RuntimeError("socket connection broken")
                print("noting sent; left to sent: ", datalen - totalsent)
                sleep(0.2)
            totalsent = totalsent + sent