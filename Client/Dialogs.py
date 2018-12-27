from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout

from GameMechanic.GameConfig import GameConfig


class JoinDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.par = parent

        self.__initUI__()


    def __initUI__(self):

        layout = QVBoxLayout(self)

        self.setLayout(layout)

        self.label1 = QLabel("IP Address:")
        layout.addWidget(self.label1)

        self.input1 = QLineEdit()
        layout.addWidget(self.input1)

        self.label2 = QLabel("Port:")
        layout.addWidget(self.label2)

        self.input2 = QLineEdit()
        layout.addWidget(self.input2)

        self.button = QPushButton("Join")
        self.button.clicked.connect(self.btnPressed)
        layout.addWidget(self.button)

        self.show()

    def btnPressed(self):
        self.par.joinPressed(self.input1.text(), int(self.input2.text()))
        self.close()


class HostDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.par = parent

        self.__initUI__()

    def __initUI__(self):
        layout = QVBoxLayout(self)

        self.setLayout(layout)

        self.label1 = QLabel("Port:")
        layout.addWidget(self.label1)

        self.input1 = QLineEdit()
        layout.addWidget(self.input1)

        self.label2 = QLabel("Number of players:")
        layout.addWidget(self.label2)

        self.input2 = QLineEdit()
        layout.addWidget(self.input2)

        self.label3 = QLabel("Number of snakes:")
        layout.addWidget(self.label3)

        self.input3 = QLineEdit()
        layout.addWidget(self.input3)

        self.label4 = QLabel("Snake size:")
        layout.addWidget(self.label4)

        self.input4 = QLineEdit()
        layout.addWidget(self.input4)

        self.label5 = QLabel("Steps per turn:")
        layout.addWidget(self.label5)

        self.input5 = QLineEdit()
        layout.addWidget(self.input5)

        self.label6 = QLabel("Turn time:")
        layout.addWidget(self.label6)

        self.input6 = QLineEdit()
        layout.addWidget(self.input6)

        self.button = QPushButton("Host")
        self.button.clicked.connect(self.btnPressed)
        layout.addWidget(self.button)

        self.show()

    def btnPressed(self):

        conf = GameConfig()

        conf.playerNumber = int(self.input2.text())
        conf.snakeNumber = int(self.input3.text())
        conf.snakeSize =  int(self.input4.text())
        conf.snakeSteps = int(self.input5.text())
        conf.turnPlanTime = float(self.input6.text())

        self.par.hostPressed(int(self.input1.text()), conf)
        self.close()
