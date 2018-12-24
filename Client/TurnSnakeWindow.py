from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.Qt import *
from GameMechanic.GridContainer import GridContainer

class TurnSnakeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #TEMP dinamicka promena velicine
        self.gridWidth = 15
        self.gridHeigth = 15
        self.gridBlockSize = 50

        self.food1src = QImage("Client\hrana1.png")
        self.food1img = self.food1src.scaled(self.gridBlockSize, self.gridBlockSize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

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
                #TEMP koristi custom QWidget
                block = QLabel()
                self.blockGrid[i].append(block)
                self.grid.addWidget(block, i, j)

        self.setWindowTitle("Turn Snake")
        self.resize(self.gridWidth * self.gridBlockSize, self.gridHeigth * self.gridBlockSize)
        self.show()

    
    def resizeEvent(self, event):
        self.gridBlockSize = self.width() / self.gridWidth
        self.food1img = self.food1src.scaled(self.gridBlockSize, self.gridBlockSize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.food1pxm = QPixmap(self.food1img)


    def update(self, gc: GridContainer):
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeigth):
                if(len(gc.blockMatrix[i][j]) == 1):
                    self.blockGrid[i][j].setPixmap(QPixmap(self.food1img))


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.bckimg = QImage("Client\pozadina.png")


    def paintEvent(self, event):
        p = QPainter(self)

        for i in range(0, self.width() // self.bckimg.width() + 1):
            for j in range(0, self.height() // self.bckimg.height() + 1):
                p.drawImage(i * self.bckimg.width(), j * self.bckimg.height(), self.bckimg)