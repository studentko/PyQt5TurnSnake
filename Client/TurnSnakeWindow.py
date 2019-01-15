from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import *

from Client.Dialogs import JoinDialog, HostDialog
from Client.UIPlayer import UIPlayer
from Client.listener import Listener
from GameMechanic.GameConfig import GameConfig
from Network.GreetingData import GreetingData
from Network.GridContainerUpdate import *
from Network.MovingPlans import *
from Client.widgets import *
from  Network.serverstarter import start_server_process, stop_server_process


class TurnSnakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gridWidth = 5
        self.gridHeight = 5
        self.gridBlockSize = 45

        self.gameRunning = False

        self.players = []

        self.blockGrid = []

        self.turnTime = 0.0
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(100)

        self.planingPhase = False

        self.loadTextures()

        self.__initUI__()

    def __initUI__(self):

        menu = self.menuBar().addMenu("Game")

        self.joinAct = QAction("&Join", self)
        self.joinAct.triggered.connect(self.join)

        self.hostAct = QAction("&Host", self)
        self.hostAct.triggered.connect(self.host)

        menu.addAction(self.joinAct)
        menu.addAction(self.hostAct)

        self.tournamentLabel = QLabel(self)
        self.tournamentLabel.setGeometry(50, 50, 200, 800)
        self.tournamentLabel.hide()
        self.centerWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)
        mainLayout = QHBoxLayout(self.centerWidget)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.centerWidget.setLayout(mainLayout)

        self.gridWidget = MainWidget()
        mainLayout.addWidget(self.gridWidget)

        self.uiWidget = QWidget(self)
        self.uiWidget.setFixedWidth(100)
        self.uiWidget.setFixedHeight(100)
        mainLayout.addWidget(self.uiWidget)

        self.uiGrid = QVBoxLayout(self)
        self.uiGrid.setAlignment(Qt.AlignTop)
        self.uiWidget.setLayout(self.uiGrid)

        self.playerColorLabel = QLabel(self)
        self.uiGrid.addWidget(self.playerColorLabel)

        self.turnTimerLabel = QLabel(self)
        self.uiGrid.addWidget(self.turnTimerLabel)

        self.gameStatusText = QLabel(self)
        self.uiGrid.addWidget(self.gameStatusText)

        self.grid = QGridLayout()
        self.gridWidget.setLayout(self.grid)
        self.grid.setSpacing(0)

        self.setWindowTitle("Turn Snake")
        self.resize(self.gridWidth * self.gridBlockSize, self.gridHeight * self.gridBlockSize)
        self.show()

    def startPlaning(self, seconds):
        self.turnTime = seconds
        self.planingPhase = True
        for player in self.players:
            player.snakeMoveLocation = []
            player.movingPlans = MovingPlans()
            for s in player.snakes:
                player.movingPlans.set_plan(s, [])
                player.snakeMoveLocation.append([s.get_head().x, s.get_head().y])
            player.selectedSnakeIndex = 0

    def endPlaningself(self):
        self.planingPhase = False

    def keyPressEvent(self, event: QKeyEvent):
        if self.planingPhase:
            if event.key() == Qt.Key_Tab:
                if len(self.players[0].snakes) > 0:
                    self.setColorStatus(self.players[0].snakes[self.players[0].selectedSnakeIndex], True)
                    self.players[0].selectedSnakeIndex = (self.players[0].selectedSnakeIndex + 1) % len(self.players[0].snakes)
            elif event.key() == Qt.Key_Space and len(self.players) == 2:
                if len(self.players[1].snakes) > 0:
                    self.setColorStatus(self.players[1].snakes[self.players[1].selectedSnakeIndex], True)
                    self.players[1].selectedSnakeIndex = (self.players[1].selectedSnakeIndex + 1) % len(self.players[1].snakes)
            else:
                if len(self.players[0].snakes) > 0:
                    snake = self.players[0].snakes[self.players[0].selectedSnakeIndex]
                    plan = self.players[0].movingPlans.get_plan(snake)
                    if event.key() == Qt.Key_D:
                        self.addPlanPoint(EMoveDirection.right, plan, snake, self.players[0])
                    elif event.key() == Qt.Key_W:
                        self.addPlanPoint(EMoveDirection.down, plan, snake, self.players[0])
                    elif event.key() == Qt.Key_A:
                        self.addPlanPoint(EMoveDirection.left, plan, snake, self.players[0])
                    elif event.key() == Qt.Key_S:
                        self.addPlanPoint(EMoveDirection.up, plan, snake, self.players[0])
                if len(self.players) == 2 and len(self.players[1].snakes) > 0:
                    snake = self.players[1].snakes[self.players[1].selectedSnakeIndex]
                    plan = self.players[1].movingPlans.get_plan(snake)
                    if event.key() == Qt.Key_Right:
                        self.addPlanPoint(EMoveDirection.right, plan, snake, self.players[1])
                    elif event.key() == Qt.Key_Up:
                        self.addPlanPoint(EMoveDirection.down, plan, snake, self.players[1])
                    elif event.key() == Qt.Key_Left:
                        self.addPlanPoint(EMoveDirection.left, plan, snake, self.players[1])
                    elif event.key() == Qt.Key_Down:
                        self.addPlanPoint(EMoveDirection.up, plan, snake, self.players[1])


    def addPlanPoint(self, moveDir, plan, snake, player):
        pos = player.snakeMoveLocation[player.selectedSnakeIndex]
        if len(plan) > 0 and (moveDir == plan[-1].getOposite()):
            self.blockGrid[pos[1]][pos[0]].texEnums.remove(EDrawable.MovePoint)
            plan.pop()
            pos[0] = (pos[0] + moveDir.x) % self.gridWidth
            pos[1] = (pos[1] + moveDir.y) % self.gridHeight
        elif len(plan) == 0 and moveDir.getOposite().getDirection() == snake.get_head().direction:
            pass
        elif len(plan) < snake.steps:
            pos[0] = (pos[0] + moveDir.x) % self.gridWidth
            pos[1] = (pos[1] + moveDir.y) % self.gridHeight
            self.blockGrid[pos[1]][pos[0]].texEnums.add(EDrawable.MovePoint)
            plan.append(moveDir)
        self.repaint()

    @pyqtSlot(GreetingData)
    def resizeBoard(self, gd: GreetingData):
        self.resizeBoardXY(gd.gridWidth, gd.gridHeight)

    def resizeBoardXY(self, x, y):

        self.gridWidth = x
        self.gridHeight = y

        self.blockGrid = []
        for i in range(0, self.gridWidth):
            self.blockGrid.append([])
            for j in range(0, self.gridHeight):
                block = BlockWidget(self.imgs, self.masks)
                self.blockGrid[i].append(block)
                self.grid.addWidget(block, i, j)

        self.resize(self.gridWidth * self.gridBlockSize + 80, self.gridHeight * self.gridBlockSize)

    def join(self):
        dialog = JoinDialog(self)
        dialog.exec()

    def joinPressed(self, address, port, p2, names):
        self.players = []
        player = UIPlayer(self, True)
        player.listen(address, port, names[0])
        self.players.append(player)
        if p2:
            player = UIPlayer(self, False)
            player.listen(address, port, names[1])
            self.players.append(player)

        self.joinAct.setEnabled(False)
        self.hostAct.setEnabled(False)
        self.setGameStatus("Waiting\nfor players")

    def host(self):
        dialog = HostDialog(self)
        dialog.exec()

    def hostPressed(self, port, gameconfig, p2, names):
        start_server_process(gameconfig, port)
        self.joinPressed("localhost", port, p2, names)

        self.joinAct.setEnabled(False)
        self.hostAct.setEnabled(False)
        self.setGameStatus("Waiting\nfor players")

    def closeEvent(self, *args, **kwargs):
        for player in self.players:
            if player.listener is not None:
                player.listener.stop()

        stop_server_process()
        self.timer.stop()

    def resizeEvent(self, event):
        self.imgs.clear()
        for i in self.imgsRaw:
            self.imgs.append(
                i.scaled(self.gridWidget.width() // self.gridWidth, self.gridWidget.height() // self.gridHeight,
                         Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.masks.clear()
        for col in self.masksRaw:
            nMasks = []
            for i in col:
                nMasks.append(
                    i.scaled(self.gridWidget.width() // self.gridWidth, self.gridWidget.height() // self.gridHeight,
                             Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.masks.append(nMasks)

    def update(self, gc: GridContainer):
        self.tournamentLabel.hide()
        self.centerWidget.show()
        if len(self.players) == 1:
            if len(self.players[0].snakes) > 0:
                self.playerColorLabel.setText(F"Player: {self.players[0].snakes[0].get_head().color.name}")
            else:
                self.playerColorLabel.setText("Player: dead")
        else:
            if len(self.players[0].snakes) > 0:
                state1 = self.players[0].snakes[0].get_head().color.name
            else:
                state1 = "dead"
            if len(self.players[1].snakes) > 0:
                state2 = self.players[1].snakes[0].get_head().color.name
            else:
                state2 = "dead"
            self.playerColorLabel.setText(F"P: {state1}, {state2}")
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeight):
                self.blockGrid[i][j].setTextures(gc.blockMatrix[i][j])
        self.repaint()

    def updateTimer(self):
        self.turnTime -= 0.1
        if (self.turnTime < 0):
            self.turnTime = 0.0

        self.turnTimerLabel.setText("Time: %.1f" % self.turnTime)

        if self.planingPhase:
            for player in self.players:
                if len(player.snakes) > 0:
                    snake = player.snakes[player.selectedSnakeIndex]
                    drawsColor = self.blockGrid[snake.get_head().y][snake.get_head().x].drawFullColor
                    self.setColorStatus(snake, not drawsColor)

    def setColorStatus(self, snake, val):
        for block in snake.blocks:
            self.blockGrid[block.y][block.x].drawFullColor = val
            self.blockGrid[block.y][block.x].repaint()

    @pyqtSlot(str)
    def setTournamentText(self, text):
        self.tournamentLabel.setText(text)
        self.centerWidget.hide()
        self.tournamentLabel.show()

    @pyqtSlot(str)
    def setGameStatus(self, text):
        self.gameStatusText.setText(text)

    def loadTextures(self):
        self.imgs = []
        self.imgsRaw = []
        self.imgsRaw.append(QImage("Client/imgs/head.png"))
        self.imgsRaw.append(QImage("Client/imgs/telo.png"))
        self.imgsRaw.append(QImage("Client/imgs/rep.png"))
        self.imgsRaw.append(QImage("Client/imgs/spoj.png"))
        self.imgsRaw.append(QImage("Client/imgs/prepreka.png"))
        self.imgsRaw.append(QImage("Client/imgs/hrana1.png"))
        self.imgsRaw.append(QImage("Client/imgs/hrana2.png"))
        self.imgsRaw.append(QImage("Client/imgs/DeusA1.png"))
        self.imgsRaw.append(QImage("Client/imgs/DeusA2.png"))
        self.imgsRaw.append(QImage("Client/imgs/kretanje.png"))

        self.masks = []
        self.masksRaw = []

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[0].append(QImage("Client/masks/head.png"))
        self.masksRaw[0].append(QImage("Client/masks/telo.png"))
        self.masksRaw[0].append(QImage("Client/masks/rep.png"))
        self.masksRaw[0].append(QImage("Client/masks/spoj.png"))
        self.masksRaw[0].append(QImage("Client/masks/prepreka.png"))
        #self.masksRaw[0].append(QImage("Client/masks/hrana1.png"))
        #self.masksRaw[0].append(QImage("Client/masks/hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[1].append(QImage("Client/masks/red/head.png"))
        self.masksRaw[1].append(QImage("Client/masks/red/telo.png"))
        self.masksRaw[1].append(QImage("Client/masks/red/rep.png"))
        self.masksRaw[1].append(QImage("Client/masks/red/spoj.png"))
        self.masksRaw[1].append(QImage("Client/masks/red/prepreka.png"))
        #self.masksRaw[1].append(QImage("Client/masks/red/hrana1.png"))
        #self.masksRaw[1].append(QImage("Client/masks/red/hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[2].append(QImage("Client/masks/blue/head.png"))
        self.masksRaw[2].append(QImage("Client/masks/blue/telo.png"))
        self.masksRaw[2].append(QImage("Client/masks/blue/rep.png"))
        self.masksRaw[2].append(QImage("Client/masks/blue/spoj.png"))
        self.masksRaw[2].append(QImage("Client/masks/blue/prepreka.png"))
        #self.masksRaw[2].append(QImage("Client/masks/blue/hrana1.png"))
        #self.masksRaw[2].append(QImage("Client/masks/blue/hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[3].append(QImage("Client/masks/yellow/head.png"))
        self.masksRaw[3].append(QImage("Client/masks/yellow/telo.png"))
        self.masksRaw[3].append(QImage("Client/masks/yellow/rep.png"))
        self.masksRaw[3].append(QImage("Client/masks/yellow/spoj.png"))
        self.masksRaw[3].append(QImage("Client/masks/yellow/prepreka.png"))
        #self.masksRaw[3].append(QImage("Client/masks/yellow/hrana1.png"))
        #self.masksRaw[3].append(QImage("Client/masks/yellow/hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[4].append(QImage("Client/masks/purple/head.png"))
        self.masksRaw[4].append(QImage("Client/masks/purple/telo.png"))
        self.masksRaw[4].append(QImage("Client/masks/purple/rep.png"))
        self.masksRaw[4].append(QImage("Client/masks/purple/spoj.png"))
        self.masksRaw[4].append(QImage("Client/masks/purple/prepreka.png"))
        #self.masksRaw[4].append(QImage("Client/masks/purple/hrana1.png"))
        #self.masksRaw[4].append(QImage("Client/masks/purple/hrana1.png"))
