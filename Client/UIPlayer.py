from PyQt5.QtCore import pyqtSlot

from Client.TurnSnakeWindow import *
from Client.listener import Listener
from Network.GridContainerUpdate import GridContainerUpdate


class UIPlayer:
    def __init__(self, window, main):
        self.snakeMoveLocation = []
        self.movingPlans = None

        self.window: TurnSnakeWindow = window
        self.main = main

        self.selectedSnakeIndex = -1
        self.snakes = []

        self.listener = None

    def listen(self, address, port):
        self.listener = Listener(self, address, port, self.main)
        self.listener.start()

        self.setListener(self.listener)

    def update(self, gc: GridContainerUpdate):
        self.snakes = gc.snakes
        for snake in self.snakes:
            self.window.setColorStatus(snake, True)

        if self.main:
            self.window.update(gc.gridContainer)

    def setListener(self, listener):
        listener.update.connect(self.update)
        listener.resize.connect(self.window.resizeBoard)
        listener.status.connect(self.window.setGameStatus)