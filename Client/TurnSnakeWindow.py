from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.Qt import *
from GameMechanic.GridContainer import GridContainer
from Client.widgets import *

class TurnSnakeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #TEMP dinamicka promena velicine
        self.gridWidth = 15
        self.gridHeigth = 15
        self.gridBlockSize = 50

        self.imgs = []
        self.imgsRaw = []
        self.imgsRaw.append(QImage("Client\\hrana1.png"))
        self.imgsRaw.append(QImage("Client\\head.png"))
        self.imgsRaw.append(QImage("Client\\telo.png"))
        self.imgsRaw.append(QImage("Client\\rep.png"))

        self.__initUI__()

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


    def update(self, gc: GridContainer):
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeigth):
                self.blockGrid[i][j].setTextures(gc.blockMatrix[i][j])
        self.repaint()

