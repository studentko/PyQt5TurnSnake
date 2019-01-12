from Network.Server import *
from GameMechanic.GameConfig import *
from multiprocessing import Process


__server_process = None


def server_main(gameConfig, port=12354, ip="0.0.0.0"):
    server = Server(gameConfig, port, ip)
    server.start_server()


def start_server_process(gameConfig, port=12354, ip="0.0.0.0"):
    global __server_process
    __server_process = Process(target=server_main, args=(gameConfig, port, ip))
    __server_process.start()


def stop_server_process():
    global __server_process
    if __server_process is not None:
        __server_process.terminate()
        __server_process = None


def join_server_process():
    __server_process.join()
