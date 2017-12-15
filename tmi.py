#The Minimalist Interface
#Inspired by Minesweeper
#Thanks for big help from Asgard Wong


from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainter, QPixmap
import sys

class Handle(QObject):
    handleMoved = pyqtSignal(QPoint)

    def __init__(self, label, xpos, ypos, radius):
        super(Handle, self).__init__()
        self.pos = QPoint(xpos, ypos)
        self.label = label
        self.radius = radius
    def __str__(self):
        stringval = "%s (%d, %d)" % (self.label, self.pos.x(), self.pos.y())
        return stringval

    def setPos(self, newpos):
        self.pos.setX(newpos.x())
        self.pos.setY(newpos.y())
        self.handleMoved.emit(self.pos)
    def x(self):
        return self.pos.x()
    def y(self):
        return self.pos.y()
    def bounds(self):
        return QRect(self.x(), self.y(), self.radius, self.radius)

class XYGraph(QWidget):
    def __init__(self, parent=None):
        super(XYGraph, self).__init__(parent)

        self.currentHandle = None
        self.dragStartPos = None
        self.setMinimumSize(800, 800)
        self.handles = [Handle('H1',100,100,100), Handle('H2',250,250,100), Handle('H3',400,400,100), Handle('H4',600,600,100)] # 4 handles each represented by a QPoint
        self.paintcounter1 = 1
        self.paintcounter2 = 1
        self.paintcounter3 = 1
        self.paintcounter4 = 1


    def paintEvent(self, event):

        qp = QPainter(self)
        firsthandle = self.handles[0]
        secondhandle = self.handles[1]
        thirdhandle = self.handles[2]
        forthhandle = self.handles[3]
        self.text1 = "img/a%d.png" % (self.paintcounter1)
        self.text2 = "img/a%d.png" % (self.paintcounter2)
        self.text3 = "img/a%d.png" % (self.paintcounter3)
        self.text4 = "img/a%d.png" % (self.paintcounter4)

        pixmap = QPixmap(self.text1)
        pos = firsthandle.pos
        qp.drawPixmap(pos.x()-pixmap.width()/2,pos.y()-pixmap.height()/2,pixmap.width(),pixmap.height(), pixmap);

        pixmap = QPixmap(self.text2)
        pos = secondhandle.pos
        qp.drawPixmap(pos.x()-pixmap.width()/2,pos.y()-pixmap.height()/2,pixmap.width(),pixmap.height(), pixmap);

        pixmap = QPixmap(self.text3)
        pos = thirdhandle.pos
        qp.drawPixmap(pos.x()-pixmap.width()/2,pos.y()-pixmap.height()/2,pixmap.width(),pixmap.height(), pixmap);

        pixmap = QPixmap(self.text4)
        pos = forthhandle.pos
        qp.drawPixmap(pos.x()-pixmap.width()/2,pos.y()-pixmap.height()/2,pixmap.width(),pixmap.height(), pixmap);


    def mousePressEvent(self, event):
        mouseX = event.pos().x()
        mouseY = event.pos().y()

        self.currentHandle = None
        for handle in self.handles:
            h = handle.bounds()
            if mouseX > h.left()-50 and mouseX < h.right()+50 and mouseY > h.top()-50 and mouseY < h.bottom()+50:

                self.currentHandle = handle
                self.dragStartPos = QPoint(handle.x(), handle.y())
                if self.currentHandle == self.handles[0]:
                    if self.paintcounter1 > 5:
                        self.paintcounter1 = 1
                    else:
                        self.paintcounter1 += 1
                if self.currentHandle == self.handles[1]:
                    if self.paintcounter2 > 5:
                        self.paintcounter2 = 1
                    else:
                        self.paintcounter2 += 1
                if self.currentHandle == self.handles[2]:
                    if self.paintcounter3 > 5:
                        self.paintcounter3 = 1
                    else:
                        self.paintcounter3 += 1
                if self.currentHandle == self.handles[3]:
                    if self.paintcounter4 > 5:
                        self.paintcounter4 = 1
                    else:
                        self.paintcounter4 += 1
                break

    def mouseMoveEvent(self, event):
        if self.currentHandle != None:
            w = self.width()
            h = self.height()
            mouse = event.pos()
            if  mouse.x() > 0 and mouse.x() < w and mouse.y() > 0 and mouse.y() < h:
                self.currentHandle.setPos(mouse)
            else:
                self.currentHandle.setPos(self.dragStartPos)
                self.dragStartPos = None
                self.currentHandle = None
            self.update()


    def mouseReleaseEvent(self, event):
        if self.currentHandle != None:
            self.currentHandle = None


class HandleLabel(QLabel):
    def __init__(self, handle):
        super(HandleLabel, self).__init__()
        self.label = handle.label


class MyWin(QWidget):
    def __init__(self):
        super(MyWin, self).__init__()
        self.initGUI()

    def initGUI(self):
        label = QLabel(self)
        self.setWindowTitle('The Minimalist Interface')
        pixmap = QPixmap('img/white_bg.png')
        label.setPixmap(pixmap)
        label.resize(pixmap.width(),pixmap.height())
        self.setGeometry(150, 150,800,800)
        self.resize(pixmap.width(),pixmap.height())
        mainlayout = QVBoxLayout()
        sublayout = QHBoxLayout()
        graph = XYGraph()

        for handle in graph.handles:
            sublayout.addWidget(HandleLabel(handle))
        mainlayout.addWidget(graph)
        mainlayout.addLayout(sublayout)
        self.setLayout(mainlayout)

        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = MyWin()
    sys.exit(app.exec_())
