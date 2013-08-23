# -*- coding: utf-8 -*-
#Ver 0.5 edited at 2013-07-25-14:23
#new version

#items needed in replay scene
#grids of map
#soldiers
#cursor

from PyQt4 import QtGui, QtCore
from basic import *
from shortest import GetRoute

TRAP_TRIGGERED = 8



UNIT_WIDTH = 100
UNIT_HEIGHT = 100
PEN_WIDTH = 0.5


LABEL_WIDTH = 100
LABEL_HEIGHT = 30
LABEL_LEFT_MARGIN = 20
DRAG_SPOT = QtCore.QPoint(20, 20)

def GetPos(mapX, mapY):
    return QtCore.QPointF(mapX*UNIT_WIDTH, mapY*UNIT_HEIGHT)
def GetGrid(corX, corY):
    x = int(corX/UNIT_WIDTH)
    y = int(corY/UNIT_HEIGHT)
    return x, y



class Ui_GridUnit(QtGui.QGraphicsObject):
    "the superclass of all grid units"
    def __init__(self, x = 0, y = 0, parent = None):
        QtGui.QGraphicsObject.__init__(self, parent)
        self.mapX = x
        self.mapY = y
        self.selected = False#no need

    def SetMapPos(self, x, y):
        self.mapX = x
        self.mapY = y
        self.setPos(self.GetPos())
    def GetPos(self):
        return GetPos(self.mapX, self.mapY)

    def SetEnabled(self, flag):
        print "fset called", flag#for test
        if (flag):
            self.setVisible(True)
            self.setEnabled(True)
        else:
            self.setEnabled(False)
            self.setVisible(False)
    def IsEnabled(self):
        return (self.isVisible() or self.isEnabled())

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        pass#

    def MousePressEvent(self, args):
        return False
    def MouseEnterEvent(self, args):
        return False
    def MouseLeaveEvent(self, args):
        return False
    def DragStartEvent(self, args):
        return False
    def DragStopEvent(self, args):
        return False
    def DragComplete(self, args):
        pass
    def DragFail(self, args):
        self.setPos(self.GetPos())
    #my event

    enability = QtCore.pyqtProperty(bool, fget = IsEnabled,
                                    fset = SetEnabled)




class Ui_MapUnit(Ui_GridUnit):
    "the unit of the map."
    def __init__(self, x, y, mapGrid, parent = None):
        Ui_GridUnit.__init__(self, x, y, parent)
        self.terrain = mapGrid.kind
        #
        #load pixmap
        #self.coverColor = None

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

    def paint(self, painter, option, widget):
        #draw pixmap
        self.GetPainter(painter)
        painter.drawRect(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT))
        #for test

    def mousePressEvent(self, event):
        self.mapGridSelected.emit(self.mapX, self.mapY)
    #old event
    def DragStopEvent(self, args):
        return True
    #my event

    mapGridSelected = QtCore.pyqtSignal(int, int)


class Ui_SoldierUnit(Ui_GridUnit):
    "the unit of the soldiers."
    def __init__(self, idNum, side, unit, parent = None):
        Ui_GridUnit.__init__(self, unit.position[0], unit.position[1], parent)
        self.type = unit.kind#?
        self.idNum = idNum
        self.side = side

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
        self.setOpacity(1-time)
    #def Flicker(self, frame):


class Ui_GridLabel(Ui_GridUnit):
    "used to show info on map grids"
    def __init__(self, text, mapX, mapY, parent = None):
        Ui_GridUnit.__init__(self, mapX, mapY, parent)
        self.text = text
        self.SetEnabled(False)#for test
        self.setPos(self.GetPos())

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

    #slots
    def ShowLabel(self, time):
        SHOW_TIME = 0.6
        DISAP_TIME = 0.9
        if (time>=SHOW_TIME):
            self.SetEnabled(True)
        if (time>=DISAP_TIME):
            self.SetEnabled(False)
        



class Ui_GridCursor(Ui_GridUnit):
    def __init__(self):
        Ui_GridUnit.__init__(self)

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
    #grid cursor
    

class Ui_MouseCursor(Ui_GridCursor):
    "the cursor moving along with mouse"
    def __init__(self):
        Ui_GridCursor.__init__(self)

        #self.isFixed = False #show whether the cursor should stop frickering
        self.timerId = self.startTimer(500)#frickering period
    def timerEvent(self, event):
        if (event.timerId()==self.timerId):
            self.setOpacity(1-self.opacity()) #make the cursor fricker
    #timer
    def MouseLeaveEvent(self, info):
        if (info.isValid and self.isEnabled()):
            x, y = info.nowPos
            self.SetMapPos(x, y)
        return True
    #my event
    #mouse cursor


class Ui_TargetCursor(Ui_GridUnit):
    "the cursor used to point out the target"
    def __init__(self):
        Ui_GridUnit.__init__(self)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        RLINE = 0.4 #rate of line
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))

#class Ui_KeyboardCursor(Ui_GridUnit):


#animation
class Ui_Animation(QtCore.QPropertyAnimation):
    def __init__(self, widget = None, prop = ""):
        QtCore.QPropertyAnimation.__init__(self, widget, prop)

    def interpolated(self, start, end, progress):
        if (start.type()==QtCore.QVariant.Bool
            and end.type()==QtCore.QVariant.Bool):
            return start
        #customed interpolator
        else:
            return QtCore.QPropertyAnimation.interpolated(self, start, end, progress)


#data of game
def ConvertTo1D(iniUnits):
    units = []
    for row in iniUnits:
        units.extend(row)
    return units

class UiD_BeginChanges:
    def __init__(self, beginInfo, cmd, endInfo, maps):
        self.templeRenew = None#

class UiD_EndChanges:
    def __init__(self, begInfo, cmd, endInfo, maps):
        self.idNum = idNum = begInfo.id[0]*len(begInfo.base[0])+begInfo.id[1]
        self.route = GetRoute(maps, begInfo.base, begInfo.id, cmd.move)
        self.order = cmd.order
        if (cmd.order==1):
            target = self.target = cmd.target[0]*len(endInfo.base[0])+cmd.target[1]
            begUnits = ConvertTo1D(begInfo.base)
            endUnits = ConvertTo1D(endInfo.base)
            self.damage = (endUnits[idNum].life-begUnits[idNum].life,
                           endUnits[target].life-begUnits[target].life) #(self, enemy)
            self.note = ["", ""]
            for i in (0, 1):
                if (self.damage[i]==0):
                    if (endInfo.attack_effect[i]==1):
                        self.note[i] = "Blocked!"
                    elif (endInfo.attack_effect[i]==0):
                        self.note[i] = "Miss"
            self.fightBack = (endInfo.attack_effect[1]!=-1) and (endUnits.life!=0)
            self.isDead = (endInfo.base[idNum].life==0, endInfo.base[target].life==0)
        elif (cmd.order==2):
            raise NotImplementedError#skill

class UiD_RoundInfo:
    "info of every round"
    def __init__(self, begInfo, cmd, endInfo, maps):
        #print len(begInfo.base[0])#for test
        self.begChanges = UiD_BeginChanges(begInfo, cmd, endInfo, maps)
        self.cmdChanges = UiD_EndChanges(begInfo, cmd, endInfo, maps)
        self.begUnits = None #if it is none, there's no changes in the unit info
        self.endUnits = ConvertTo1D(endInfo.base)
        self.idNum = begInfo.id[0]*len(endInfo.base[0])+begInfo.id[1]
        self.score = endInfo.score

class UiD_BattleData:
    "info of the entire battle(not completed)"
    def __init__(self, iniInfo, begInfo):
        self.map = iniInfo.map
        self.side0SoldierNum = len(iniInfo.base[0])
        self.iniUnits = ConvertTo1D(iniInfo.base)
        self.roundInfo = []
        self.nextRoundInfo = begInfo #temporary stores the round_begin_info
        self.result = None #result
