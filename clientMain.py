from PyQt5.QtWidgets import QApplication
from Client.TurnSnakeWindow import *
from GameMechanic.LevelController import LevelController
from Client.listener import *
import time
import sys

if __name__ == "__main__":
    app = QApplication([])
    turnSnake = TurnSnakeWindow()

    """listener = Listener(turnSnake)
    listener.start()

    turnSnake.setListener(listener)"""

    app.exec_()