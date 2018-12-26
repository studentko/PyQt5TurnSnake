from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import *
from Network.GridContainerUpdate import *
from Network.MovingPlans import *
from Client.widgets import *

class TurnSnakeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #TEMP dinamicka promena velicine
        self.gridWidth = 15
        self.gridHeigth = 15
        self.gridBlockSize = 50

        self.planingPhase = False
        self.selectedSnakeIndex = -1
        self.snakes = []

        self.imgs = []
        self.imgsRaw = []
        self.imgsRaw.append(QImage("Client\\hrana1.png"))
        self.imgsRaw.append(QImage("Client\\head.png"))
        self.imgsRaw.append(QImage("Client\\telo.png"))
        self.imgsRaw.append(QImage("Client\\rep.png"))
        self.imgsRaw.append(QImage("Client\\spoj.png"))
        self.imgsRaw.append(QImage("Client\\prepreka.png"))
        self.imgsRaw.append(QImage("Client\\kretanje.png"))

        self.__initUI__()


    def setListener(self, listener):
        listener.update.connect(self.update)


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

        centerWidget = MainWidget()
        self.setCentralWidget(centerWidget)

        self.grid = QGridLayout()
        centerWidget.setLayout(self.grid)
        self.grid.setSpacing(0)

        self.blockGrid = []
        for i in range(0, self.gridWidth):
            self.blockGrid.append([])
            for j in range(0, self.gridHeigth):
                block = BlockWidget(self.imgs)
                self.blockGrid[i].append(block)
                self.grid.addWidget(block, i, j)

        self.setWindowTitle("Turn Snake")
        self.resize(self.gridWidth * self.gridBlockSize, self.gridHeigth * self.gridBlockSize)
        self.show()
        
    
    def resizeEvent(self, event):
        self.imgs.clear()
        for i in self.imgsRaw:
            self.imgs.append(i.scaled(self.width() // self.gridWidth, self.height() // self.gridHeigth, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))


    @pyqtSlot(GridContainerUpdate)
    def update(self, gc: GridContainerUpdate):
        self.snakes = gc.snakes
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeigth):
                self.blockGrid[i][j].setTextures(gc.gridContainer.blockMatrix[i][j])
        self.repaint()

