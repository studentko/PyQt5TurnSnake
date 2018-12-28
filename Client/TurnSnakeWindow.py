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
        self.gridBlockSize = 50

        self.planingPhase = False
        self.selectedSnakeIndex = -1
        self.snakes = []

        self.loadTextures()

        self.listener = None

        self.__initUI__()


    def setListener(self, listener):
        listener.update.connect(self.update)
        listener.resize.connect(self.resizeBoard)


    def startPlaning(self, seconds):
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
        if(self.planingPhase):
            if(event.key() == Qt.Key_Tab):
                self.selectedSnakeIndex = (self.selectedSnakeIndex + 1) % len(self.snakes)
            else:
                snake = self.snakes[self.selectedSnakeIndex]
                plan = self.moveingPlans.get_plan(snake)
                if(event.key() == Qt.Key_D):
                    self.addPlanPoint(EMoveDirection.right, plan, snake)
                elif(event.key() == Qt.Key_W):
                    self.addPlanPoint(EMoveDirection.down, plan, snake)
                elif(event.key() == Qt.Key_A):
                    self.addPlanPoint(EMoveDirection.left, plan, snake)
                elif(event.key() == Qt.Key_S):
                    self.addPlanPoint(EMoveDirection.up, plan, snake)


    def addPlanPoint(self, moveDir, plan, snake):
        pos = self.snakeMoveLocation[self.selectedSnakeIndex]
        if (len(plan) > 0 and (moveDir == plan[-1].getOposite())):
            self.blockGrid[pos[1]][pos[0]].texEnums.remove(EDrawable.MovePoint)
            plan.pop()
            pos[0] = (pos[0] + moveDir.x) % self.gridWidth
            pos[1] = (pos[1] + moveDir.y) % self.gridHeigth
        elif(len(plan) < snake.steps):
            pos[0] = (pos[0] + moveDir.x) % self.gridWidth
            pos[1] = (pos[1] + moveDir.y) % self.gridHeigth
            self.blockGrid[pos[1]][pos[0]].texEnums.add(EDrawable.MovePoint)
            plan.append(moveDir)
        self.repaint()



    def __initUI__(self):

        menu = self.menuBar().addMenu("Game")

        joinAct = QAction("&Join", self)
        joinAct.triggered.connect(self.join)

        hostAct = QAction("&Host", self)
        hostAct.triggered.connect(self.host)

        menu.addAction(joinAct)
        menu.addAction(hostAct)

        centerWidget = MainWidget()
        self.setCentralWidget(centerWidget)

        self.grid = QGridLayout()
        centerWidget.setLayout(self.grid)
        self.grid.setSpacing(0)

        self.setWindowTitle("Turn Snake")
        self.resize(self.gridWidth * self.gridBlockSize, self.gridHeigth * self.gridBlockSize)
        self.show()



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

        self.resize(self.gridWidth * self.gridBlockSize, self.gridHeigth * self.gridBlockSize)


    def join(self):
        dialog = JoinDialog(self)
        dialog.exec()


    def joinPressed(self, address, port):
        self.listener = Listener(self, address, port)
        self.listener.start()

        self.setListener(self.listener)

    def host(self):
        dialog = HostDialog(self)
        dialog.exec()

    def hostPressed(self, port, gameconfig):
        start_server_process(gameconfig, port)
        self.joinPressed("localhost", port)


    def closeEvent(self, *args, **kwargs):
        if(self.listener is not None):
            self.listener.stop()

        stop_server_process()
        
    
    def resizeEvent(self, event):
        self.imgs.clear()
        for i in self.imgsRaw:
            self.imgs.append(i.scaled(self.width() // self.gridWidth, self.height() // self.gridHeigth, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.masks.clear()
        for col in self.masksRaw:
            nMasks = []
            for i in col:
                nMasks.append(i.scaled(self.width() // self.gridWidth, self.height() // self.gridHeigth, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.masks.append(nMasks)


    @pyqtSlot(GridContainerUpdate)
    def update(self, gc: GridContainerUpdate):
        self.snakes = gc.snakes
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeigth):
                self.blockGrid[i][j].setTextures(gc.gridContainer.blockMatrix[i][j])
        self.repaint()


    def loadTextures(self):
        self.imgs = []
        self.imgsRaw = []
        self.imgsRaw.append(QImage("Client\\imgs\\head.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\telo.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\rep.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\spoj.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\prepreka.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\hrana1.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\hrana1.png"))
        self.imgsRaw.append(QImage("Client\\imgs\\kretanje.png"))

        self.masks = []
        self.masksRaw = []

        self.masksRaw.append([])
        self.masks.append([])


        self.masksRaw[0].append(QImage("Client\\masks\\head.png"))
        self.masksRaw[0].append(QImage("Client\\masks\\telo.png"))
        self.masksRaw[0].append(QImage("Client\\masks\\rep.png"))
        self.masksRaw[0].append(QImage("Client\\masks\\spoj.png"))
        self.masksRaw[0].append(QImage("Client\\masks\\prepreka.png"))
        self.masksRaw[0].append(QImage("Client\\masks\\hrana1.png"))
        self.masksRaw[0].append(QImage("Client\\masks\\hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[1].append(QImage("Client\\masks\\red\\head.png"))
        self.masksRaw[1].append(QImage("Client\\masks\\red\\telo.png"))
        self.masksRaw[1].append(QImage("Client\\masks\\red\\rep.png"))
        self.masksRaw[1].append(QImage("Client\\masks\\red\\spoj.png"))
        self.masksRaw[1].append(QImage("Client\\masks\\red\\prepreka.png"))
        self.masksRaw[1].append(QImage("Client\\masks\\red\\hrana1.png"))
        self.masksRaw[1].append(QImage("Client\\masks\\red\\hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[2].append(QImage("Client\\masks\\blue\\head.png"))
        self.masksRaw[2].append(QImage("Client\\masks\\blue\\telo.png"))
        self.masksRaw[2].append(QImage("Client\\masks\\blue\\rep.png"))
        self.masksRaw[2].append(QImage("Client\\masks\\blue\\spoj.png"))
        self.masksRaw[2].append(QImage("Client\\masks\\blue\\prepreka.png"))
        self.masksRaw[2].append(QImage("Client\\masks\\blue\\hrana1.png"))
        self.masksRaw[2].append(QImage("Client\\masks\\blue\\hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\head.png"))
        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\telo.png"))
        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\rep.png"))
        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\spoj.png"))
        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\prepreka.png"))
        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\hrana1.png"))
        self.masksRaw[3].append(QImage("Client\\masks\\yellow\\hrana1.png"))

        self.masksRaw.append([])
        self.masks.append([])

        self.masksRaw[4].append(QImage("Client\\masks\\purple\\head.png"))
        self.masksRaw[4].append(QImage("Client\\masks\\purple\\telo.png"))
        self.masksRaw[4].append(QImage("Client\\masks\\purple\\rep.png"))
        self.masksRaw[4].append(QImage("Client\\masks\\purple\\spoj.png"))
        self.masksRaw[4].append(QImage("Client\\masks\\purple\\prepreka.png"))
        self.masksRaw[4].append(QImage("Client\\masks\\purple\\hrana1.png"))
        self.masksRaw[4].append(QImage("Client\\masks\\purple\\hrana1.png"))