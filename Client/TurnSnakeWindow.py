from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import *

from Client.Dialogs import JoinDialog, HostDialog
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
        self.gridHeigth = 5
        self.gridBlockSize = 45

        self.gameRunnung = False

        self.blockGrid = []
        self.snakeMoveLocation = []
        self.moveingPlans = None

        self.turnTime = 0.0
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(100)

        self.planingPhase = False
        self.selectedSnakeIndex = -1
        self.snakes = []

        self.loadTextures()

        self.listener = None

        self.__initUI__()

    def __initUI__(self):

        menu = self.menuBar().addMenu("Game")

        self.joinAct = QAction("&Join", self)
        self.joinAct.triggered.connect(self.join)

        self.hostAct = QAction("&Host", self)
        self.hostAct.triggered.connect(self.host)

        menu.addAction(self.joinAct)
        menu.addAction(self.hostAct)

        centerWidget = QWidget(self)
        self.setCentralWidget(centerWidget)
        mainLayout = QHBoxLayout(centerWidget)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        centerWidget.setLayout(mainLayout)

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
        self.resize(self.gridWidth * self.gridBlockSize, self.gridHeigth * self.gridBlockSize)
        self.show()

    def setListener(self, listener):
        listener.update.connect(self.update)
        listener.resize.connect(self.resizeBoard)
        listener.status.connect(self.setGameStatus)

    def startPlaning(self, seconds):
        self.turnTime = seconds
        self.planingPhase = True
        self.moveingPlans = MovingPlans()
        self.snakeMoveLocation = []
        for s in self.snakes:
            self.moveingPlans.set_plan(s, [])
            self.snakeMoveLocation.append([s.get_head().x, s.get_head().y])
        self.selectedSnakeIndex = 0

    def endPlaningAndGetPlans(self) -> MovingPlans:
        self.planingPhase = False
        return self.moveingPlans

    def keyPressEvent(self, event: QKeyEvent):
        if self.planingPhase:
            if event.key() == Qt.Key_Tab:
                self.setColorStatus(self.snakes[self.selectedSnakeIndex], True)
                self.selectedSnakeIndex = (self.selectedSnakeIndex + 1) % len(self.snakes)
            else:
                if len(self.snakes) > 0:
                    snake = self.snakes[self.selectedSnakeIndex]
                    plan = self.moveingPlans.get_plan(snake)
                    if event.key() == Qt.Key_D:
                        self.addPlanPoint(EMoveDirection.right, plan, snake)
                    elif event.key() == Qt.Key_W:
                        self.addPlanPoint(EMoveDirection.down, plan, snake)
                    elif event.key() == Qt.Key_A:
                        self.addPlanPoint(EMoveDirection.left, plan, snake)
                    elif event.key() == Qt.Key_S:
                        self.addPlanPoint(EMoveDirection.up, plan, snake)

    def addPlanPoint(self, moveDir, plan, snake):
        pos = self.snakeMoveLocation[self.selectedSnakeIndex]
        if len(plan) > 0 and (moveDir == plan[-1].getOposite()):
            self.blockGrid[pos[1]][pos[0]].texEnums.remove(EDrawable.MovePoint)
            plan.pop()
            pos[0] = (pos[0] + moveDir.x) % self.gridWidth
            pos[1] = (pos[1] + moveDir.y) % self.gridHeigth
        elif len(plan) == 0 and moveDir.getOposite().getDirection() == snake.get_head().direction:
            pass
        elif len(plan) < snake.steps:
            pos[0] = (pos[0] + moveDir.x) % self.gridWidth
            pos[1] = (pos[1] + moveDir.y) % self.gridHeigth
            self.blockGrid[pos[1]][pos[0]].texEnums.add(EDrawable.MovePoint)
            plan.append(moveDir)
        self.repaint()

    @pyqtSlot(GreetingData)
    def resizeBoard(self, gd: GreetingData):
        self.resizeBoardXY(gd.gridWidth, gd.gridHeight)

    def resizeBoardXY(self, x, y):

        self.gridWidth = x
        self.gridHeigth = y

        self.blockGrid = []
        for i in range(0, self.gridWidth):
            self.blockGrid.append([])
            for j in range(0, self.gridHeigth):
                block = BlockWidget(self.imgs, self.masks)
                self.blockGrid[i].append(block)
                self.grid.addWidget(block, i, j)

        self.resize(self.gridWidth * self.gridBlockSize + 80, self.gridHeigth * self.gridBlockSize)

    def join(self):
        dialog = JoinDialog(self)
        dialog.exec()

    def joinPressed(self, address, port):
        self.listener = Listener(self, address, port)
        self.listener.start()

        self.setListener(self.listener)

        self.joinAct.setEnabled(False)
        self.hostAct.setEnabled(False)
        self.setGameStatus("Waiting\nfor players")

    def host(self):
        dialog = HostDialog(self)
        dialog.exec()

    def hostPressed(self, port, gameconfig):
        start_server_process(gameconfig, port)
        self.joinPressed("localhost", port)

        self.joinAct.setEnabled(False)
        self.hostAct.setEnabled(False)
        self.setGameStatus("Waiting\nfor players")

    def closeEvent(self, *args, **kwargs):
        if self.listener is not None:
            self.listener.stop()

        stop_server_process()
        self.timer.stop()

    def resizeEvent(self, event):
        self.imgs.clear()
        for i in self.imgsRaw:
            self.imgs.append(
                i.scaled(self.gridWidget.width() // self.gridWidth, self.gridWidget.height() // self.gridHeigth,
                         Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.masks.clear()
        for col in self.masksRaw:
            nMasks = []
            for i in col:
                nMasks.append(
                    i.scaled(self.gridWidget.width() // self.gridWidth, self.gridWidget.height() // self.gridHeigth,
                             Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.masks.append(nMasks)

    @pyqtSlot(GridContainerUpdate)
    def update(self, gc: GridContainerUpdate):
        self.snakes = gc.snakes
        for snake in self.snakes:
            self.setColorStatus(snake, True)
        if len(self.snakes) > 0:
            self.playerColorLabel.setText(F"Player: {self.snakes[0].get_head().color.name}")
        else:
            self.playerColorLabel.setText("Player: dead")
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeigth):
                self.blockGrid[i][j].setTextures(gc.gridContainer.blockMatrix[i][j])
        self.repaint()

    def updateTimer(self):
        self.turnTime -= 0.1
        if (self.turnTime < 0):
            self.turnTime = 0.0

        self.turnTimerLabel.setText("Time: %.1f" % self.turnTime)

        if self.planingPhase and len(self.snakes) > 0:
            snake = self.snakes[self.selectedSnakeIndex]
            drawsColor = self.blockGrid[snake.get_head().y][snake.get_head().x].drawFullColor
            self.setColorStatus(snake, not drawsColor)

    def setColorStatus(self, snake, val):
        for block in snake.blocks:
            self.blockGrid[block.y][block.x].drawFullColor = val
            self.blockGrid[block.y][block.x].repaint()

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
