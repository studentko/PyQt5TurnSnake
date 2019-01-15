from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QCheckBox

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
        self.input1.setText("localhost")
        layout.addWidget(self.input1)

        self.label2 = QLabel("Port:")
        layout.addWidget(self.label2)

        self.input2 = QLineEdit()
        self.input2.setText("12355")
        layout.addWidget(self.input2)

        self.label3 = QLabel("Player name:")
        layout.addWidget(self.label3)

        self.input3 = QLineEdit()
        self.input3.setText("")
        layout.addWidget(self.input3)

        self.button = QPushButton("Join")
        self.button.clicked.connect(self.btnPressed)
        layout.addWidget(self.button)

        self.show()

    def btnPressed(self):
        self.par.joinPressed(self.input1.text(), int(self.input2.text()), False, [self.input3.text()])
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
        self.input1.setText("12355")
        layout.addWidget(self.input1)

        self.label2 = QLabel("Number of players:")
        layout.addWidget(self.label2)

        self.input2 = QLineEdit()
        self.input2.setText("2")
        layout.addWidget(self.input2)

        self.label3 = QLabel("Number of snakes:")
        layout.addWidget(self.label3)

        self.input3 = QLineEdit()
        self.input3.setText("1")
        layout.addWidget(self.input3)

        self.label4 = QLabel("Snake size:")
        layout.addWidget(self.label4)

        self.input4 = QLineEdit()
        self.input4.setText("3")
        layout.addWidget(self.input4)

        self.label5 = QLabel("Steps per turn:")
        layout.addWidget(self.label5)

        self.input5 = QLineEdit()
        self.input5.setText("5")
        layout.addWidget(self.input5)

        self.label6 = QLabel("Turn time:")
        layout.addWidget(self.label6)

        self.input6 = QLineEdit()
        self.input6.setText("5.0")
        layout.addWidget(self.input6)

        self.chbox = QCheckBox()
        self.chbox.setText("Tournament")
        self.chbox.stateChanged.connect(self.tournamentChecked)
        layout.addWidget(self.chbox)

        self.label7 = QLabel("Player names:")
        layout.addWidget(self.label7)

        self.input7 = QLineEdit()
        self.input7.setText("")
        layout.addWidget(self.input7)

        self.input8 = QLineEdit()
        self.input8.setText("")
        layout.addWidget(self.input8)

        self.mpc = QCheckBox()
        self.mpc.setText("2 Player")
        self.mpc.stateChanged.connect(self.mcpChecked)
        layout.addWidget(self.mpc)

        self.button = QPushButton("Host")
        self.button.clicked.connect(self.btnPressed)
        layout.addWidget(self.button)

        self.show()

    def btnPressed(self):
        conf = GameConfig()

        conf.playerNumber = int(self.input2.text())
        conf.snakeNumber = int(self.input3.text())
        conf.snakeSize = int(self.input4.text())
        conf.snakeSteps = int(self.input5.text())
        conf.turnPlanTime = float(self.input6.text())
        conf.tournament = self.chbox.isChecked()

        self.par.hostPressed(int(self.input1.text()), conf, self.mpc.isChecked(), [self.input7.text(), self.input8.text()])
        self.close()

    def tournamentChecked(self, state):
        if state == Qt.Checked:
            self.mpc.setEnabled(False)
            self.mpc.setChecked(False)
            self.input8.setEnabled(False)
        else:
            self.mpc.setEnabled(True)
            self.input8.setEnabled(True)

    def mcpChecked(self, state):
        if state == Qt.Checked:
            self.chbox.setChecked(False)
            self.chbox.setEnabled(False)
        else:
            self.chbox.setEnabled(True)