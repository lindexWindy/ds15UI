# -*- coding: utf-8 -*-
#Ver 0.5 edited at 2013-07-25-14:23
#Changes: some bugs in the cursor class
#Changes: mouse press events, small change in __init__

#items needed in replay scene
#grids of map
#soldiers
#cursor

from PyQt4 import QtGui, QtCore
from basic import *

TRAP_TRIGGERED = 8



UNIT_WIDTH = 100
UNIT_HEIGHT = 100
PEN_WIDTH = 0.5


LABEL_WIDTH = 100
LABEL_HEIGHT = 30
LABEL_LEFT_MARGIN = 20

def GetPos(mapX, mapY):
    return QtCore.QPointF(mapX*UNIT_WIDTH, mapY*UNIT_HEIGHT)

class Ui_MapUnit(QtGui.QGraphicsObject):
    "the unit of the map. Generalized."
    def __init__(self, x, y, mapGrid, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.mapX = x
        self.mapY = y
        self.terrain = mapGrid.kind
        #load pixmap
        self.selected = False
        self.coverColor = None

    #def GetImage(self, painter, image):
    def GetPainter(self, painter):
        "change the painter according to the terrain, selection state, etc"
        terrainColor = {PLAIN:QtGui.QColor(205, 173, 0), MOUNTAIN:QtGui.QColor(139, 105, 20),
                        FOREST:QtGui.QColor(0, 139, 0), BARRIER:QtGui.QColor(139, 126, 102),
                        TURRET:QtGui.QColor(255, 0, 0), TRAP:QtGui.QColor(139, 0, 0),
                        TEMPLE:QtGui.QColor(0, 0, 139), GEAR:QtGui.QColor(139, 101, 8)}
        brush = QtGui.QBrush()
        brush.setColor(terrainColor[self.terrain])
        brush.setStyle(QtCore.Qt.SolidPattern)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0, 0, 0))
        pen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(pen)
        painter.setBrush(brush)
        #for test

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        #draw pixmap
        self.GetPainter(painter)
        painter.drawRect(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT))
        #for test

    def mousePressEvent(self, event):
        self.mapGridSelected.emit(self.mapX, self.mapY)

    mapGridSelected = QtCore.pyqtSignal(int, int)


class Ui_SoldierUnit(QtGui.QGraphicsObject):
    "the unit of the soldiers. Generalized."
    def __init__(self, idNum, side, unit, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.mapX = unit.position[0]
        self.mapY = unit.position[1]
        self.type = unit.kind
        self.idNum = idNum
        self.side = side
        self.selected = False

    def SetMapPos(self, x, y):
        self.mapX = x
        self.mapY = y
    def GetPos(self):
        return GetPos(self.mapX, self.mapY)

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        imageRoute = {SABER:"saber.png",
                     LANCER:"lancer.png",
                     ARCHER:"archer.png",
                     DRAGON_RIDER:"dragonrider.png",
                     WARRIOR:"warrior.png",
                     WIZARD:"wizard.png",
                     HERO_1:"hero1.png"}
        fileRoute = "SoldierImage\\"
        image = QtGui.QImage(fileRoute+imageRoute[self.type])
        painter.setCompositionMode(painter.CompositionMode_Multiply)
        painter.drawImage(QtCore.QRectF(0, 0, UNIT_WIDTH, UNIT_HEIGHT), image)

    def mousePressEvent(self, event):
        self.soldierSelected.emit(self.idNum)

    soldierSelected = QtCore.pyqtSignal(int)

    #slots for creating animation
    def FadeOut(self, time):
        print time#for test
        self.setOpacity(1-time)
    #def Flicker(self, frame):


class Ui_GridLabel(QtGui.QGraphicsObject):
    "used to show info on map grids"
    def __init__(self, text, mapX, mapY, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.text = text
        self.mapX = mapX
        self.mapY = mapY

    def boundingRect(self):
        return QtCore.QRectF(LABEL_LEFT_MARGIN-PEN_WIDTH, 0-LABEL_HEIGHT-PEN_WIDTH,
                             LABEL_WIDTH+PEN_WIDTH, LABEL_HEIGHT+PEN_WIDTH)
        #regard the downleft corner as origin

    def paint(self, painter, option, widget):
        font = QtGui.QFont("Times New Roman", 20)
        #font.setColor(QtGui.QColor(0, 0, 0))
        painter.setFont(font)
        #painter.setColor(QtGui.QColor(0, 0, 0))
        painter.drawText(QtCore.QPointF(LABEL_LEFT_MARGIN, 0), self.text)
        

class Ui_GridCursor(QtGui.QGraphicsObject):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)

        self.isFixed = False #show whether the cursor should stop frickering
        self.timerId = self.startTimer(500)#frickering period

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        RLINE = 0.4 #rate of line
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, RLINE*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RLINE*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RLINE*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RLINE)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RLINE)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RLINE*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RLINE)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RLINE)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))

    #def mousePressEvent(self, event):
        #event.ignore()
    #cursor
    def timerEvent(self, event):
        if (event.timerId()==self.timerId):
            self.setOpacity(1-self.opacity()) #make the cursor fricker


