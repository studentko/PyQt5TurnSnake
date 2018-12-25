from PyQt5.QtCore import QThread
from Network.Client import *
from Network.NetworkCommand import ENetworkCommand
from Client.TurnSnakeWindow import *

class Listener(QObject):

    finished = pyqtSignal()
    update = pyqtSignal(GridContainerUpdate)

    def __init__(self):
        super().__init__()
    
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


    @pyqtSlot()
    def run(self):
        client = Client("localhost", 12355)

        client.connect()

        while True:
            command = client.get_command()
            if(command.comm == ENetworkCommand.greeting):
                self.playerId = command.data
            elif(command.comm == ENetworkCommand.container_update):
                self.update.emit(command.data)
                self.snakes = command.data.snakes
            elif(command.comm == ENetworkCommand.call_for_plans):
                temp = MovingPlans()
                for s in self.snakes:
                    moves = []
                    for _ in range(s.steps):
                        moves.append(s.lastStepDirection)
                    temp.set_plan(s, moves)
                client.send_plans(temp)