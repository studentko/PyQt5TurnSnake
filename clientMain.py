from PyQt5.QtWidgets import QApplication
from Client.TurnSnakeWindow import *
from GameMechanic.LevelController import LevelController
import time
import sys

if __name__ == "__main__":
    app = QApplication([])
    turnSnake = TurnSnakeWindow()
    lc = LevelController()
    turnSnake.update(lc.gridContainer)
    app.exec_()