from PyQt5.QtCore import QThread
from Network.Client import *
from Network.NetworkCommand import ENetworkCommand
from Client.TurnSnakeWindow import *
from Network.GridContainerUpdate import *
from Network.GreetingData import *

class Listener(QObject):

    finished = pyqtSignal()
    update = pyqtSignal(GridContainerUpdate)
    resize = pyqtSignal(GreetingData)
    status = pyqtSignal(str)

    def __init__(self, tsWin, address, port):
        super().__init__()
        self.tsWin = tsWin
        self.address = address
        self.port = port
    
        self.snakes = []

        self.thread = QThread()
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Worker Signals to the Thread slots
        self.finished.connect(self.thread.quit)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.run)


    def start(self):
        # Start the thread
        self.thread.start()
        print("Thread_Start")

    def stop(self):
        self.thread.terminate()


    @pyqtSlot()
    def run(self):

        print("Thread_Running")

        client = Client(self.address, self.port)

        client.connect()

        while True:
            command = client.get_command()
            if(command.comm == ENetworkCommand.greeting):
                self.resize.emit(command.data)
            elif(command.comm == ENetworkCommand.container_update):
                self.update.emit(command.data)
                self.snakes = command.data.snakes
            elif(command.comm == ENetworkCommand.turn_count_start):
                self.tsWin.startPlaning(command.data)
                self.status.emit("")
            elif(command.comm == ENetworkCommand.call_for_plans):
                client.send_plans(self.tsWin.endPlaningAndGetPlans())