from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtGui import QImage, QPainter, QBrush, QColor
from GameMechanic.BaseBlock import *

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.bckimg = QImage("Client\pozadina.png")


    def paintEvent(self, event):
        p = QPainter(self)

        for i in range(0, self.width() // self.bckimg.width() + 1):
            for j in range(0, self.height() // self.bckimg.height() + 1):
                p.drawImage(i * self.bckimg.width(), j * self.bckimg.height(), self.bckimg)


class BlockWidget(QWidget):
    def __init__(self, imgs):
        super().__init__()
        self.texEnums = []
        self.imgs = imgs


    def setTextures(self, texEnums):
        self.texEnums = texEnums


    def paintEvent(self, event):
        p = QPainter(self)
        r: QRect = event.rect()

        for i in self.texEnums:
            if(isinstance(i, BaseBlock)):
                p.translate(r.width() / 2, r.height() / 2)
                if(i.direction == 90 or i.direction == 270):
                    r.setRect(0, 0, r.height(), r.width())
                p.rotate(i.direction)
                p.translate(-r.width() / 2, -r.height() / 2)
                p.drawImage(r, self.imgs[i.getDrawable()])
            else:
                p.drawImage(r.x(), r.y(), self.imgs[i])

