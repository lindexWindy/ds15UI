# -*- coding: utf-8 -*-
#new version

from Ui_UnitsNew import *
from Ui_Error import Ui_Error
import sys, math

class Ui_MouseInfo:
    def __init__(self, view, event):
        if (not issubclass(view.__class__, Ui_View)):
            pass#raise error
        self.nowCoor = view.mapToScene(event.pos())
        self.initPos = view.nowPos
        self.nowPos = GetGrid(self.nowCoor.x(), self.nowCoor.y())
        self.isValid = True
        if (self.nowPos[0]<0 or self.nowPos[1]<0 or
            self.nowPos[0]>=view.mapSize[0] or self.nowPos[1]>=view.mapSize[0]):
            self.nowPos = self.initPos
            self.isValid = False
        self.eventType = event.type()
        self.eventButton = event.buttons()




class Ui_View(QtGui.QGraphicsView):
    def __init__(self, scene, parent = None):
        QtGui.QGraphicsView.__init__(self, scene, parent)
        self.unitMap = {}
        self.mapSize = (0, 0)
        self.nowPos = (0, 0)
        self.nowFocus = (0, 0)##
        self.dragUnit = None

    def Initialize(self, mapSizeX, mapSizeY):
        self.mapSize = (mapSizeX, mapSizeY)
        self.unitMap.clear()
        for x in range(mapSizeX):
            for y in range(mapSizeY):
                self.unitMap[(x, y)] = []

    def AddItem(self, item):
        item.hashIndex = (item.mapX, item.mapY)
        self.unitMap[item.hashIndex].append(item)
        self.scene().addItem(item)
    def RemoveItem(self, item):
        self.unitMap[item.hashIndex].remove(item)
        del item.hashIndex
        self.scene().removeItem(item)
    def UpdateHash(self, pos):
        newHash = []
        for item in self.unitMap[pos]:
            if ((item.mapX, item.mapY)==pos):
                newHash.append(item)
            else:
                self.unitMap[(item.mapX, item.mapY)].append(item)
        self.unitMap[pos] = newHash
    #if bug appears, consider the z value

    def RaiseEvent(self, pos, eventType, args):
        l = len(self.unitMap[pos])
        while (l>0):
            l -= 1
            if (eventType==self.MOUSE_PRESS_EVENT):
                result = self.unitMap[pos][l].MousePressEvent(args)
            elif (eventType==self.ENTER_EVENT):
                result = self.unitMap[pos][l].MouseEnterEvent(args)
            elif (eventType==self.LEAVE_EVENT):
                result = self.unitMap[pos][l].MouseLeaveEvent(args)
            elif (eventType==self.DRAG_START_EVENT):
                result = self.unitMap[pos][l].DragStartEvent(args)
            elif (eventType==self.DRAG_STOP_EVENT):
                result = self.unitMap[pos][l].DragStopEvent(args)
            if (result):
                return result

    def mousePressEvent(self, event):
        print "MousePressEvent called"#for test
        self.MouseEvent(event)
    def mouseReleaseEvent(self, event):
        print "MouseReleaseEvent called"#for test
        self.MouseEvent(event)
    def mouseMoveEvent(self, event):
        print "MouseMoveEvent called"#for test
        self.MouseEvent(event)
    #transformer
    
    def MouseEvent(self, event):
        print "MouseEvent called"#for test
        info = Ui_MouseInfo(self, event)
        self.nowPos = info.nowPos
        if (info.eventType==QtCore.QEvent.MouseButtonPress and
            (info.eventButton & QtCore.Qt.LeftButton)):
            self.RaiseEvent(info.nowPos, self.MOUSE_PRESS_EVENT, info)
            #handles the mouse press event
            self.dragUnit = self.RaiseEvent(info.nowPos, self.DRAG_START_EVENT, info)
            #starts a drag
        elif (info.eventType==QtCore.QEvent.MouseButtonRelease and
              (info.eventButton & QtCore.Qt.LeftButton)):
            if (self.dragUnit!=None):
                if (self.unitMap[info.nowPos]==[] or
                    self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.dragUnit, info))):
                    self.dragUnit.DragComplete(info)
                else:
                    pass#drag fails
            self.dragUnit = None
            #handles the drop event
        elif (info.eventType==QtCore.QEvent.MouseMove):
            if (self.dragUnit!=None):
                dragUnit.setPos(info.nowCoor)#handles the drag-move event
                self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.dragUnit, info))
            else:
                if (info.initPos!=info.nowPos):
                    self.RaiseEvent(info.initPos, self.LEAVE_EVENT, info)
                    self.RaiseEvent(info.nowPos, self.ENTER_EVENT, info)
                #handles the enter and the leave event
                #如果鼠标在拖放状态下移出widget外怎么办？
        self.UpdateHash(info.initPos)
        self.UpdateHash(info.nowPos)
        #updates the hash map
    #handles seperatedly or together?
            
    #def keyPressEvent(self, event):

    MOUSE_PRESS_EVENT = 1
    DRAG_START_EVENT = 2
    DRAG_STOP_EVENT = 3
    LEAVE_EVENT = 4
    ENTER_EVENT = 5



##############################################################

class Ui_ReplayView(Ui_View):
    "the replay graphic view"
    def __init__(self, scene, parent = None):
        Ui_View.__init__(self, scene, parent)
        self.mapItem = []
        self.soldierItem = []
        self.soldierAlive = []
        self.sizeX = 0
        self.sizeY = 0
        #ini of items
        self.cursor = None
        #ini of the cursor
        self.movTimeline = QtCore.QTimeLine()
        self.atkTimeline = QtCore.QTimeLine()
        self.dieTimeline = QtCore.QTimeLine()
        self.animation = QtGui.QGraphicsItemAnimation()
        self.label = Ui_GridLabel("", 0, 0)
        #ini of the animation
    def Initialize(self, maps, units, side0 = 0,
                   MapUnit = Ui_MapUnit, SoldierUnit = Ui_SoldierUnit, Cursor = Ui_MouseCursor):
        if (not (issubclass(MapUnit, Ui_MapUnit)
                 and issubclass(SoldierUnit, Ui_SoldierUnit)
                 and issubclass(Cursor, Ui_GridUnit))):
            print "error"#raise error
        #check the type
        scene = self.scene()
        for item in scene.items():
            scene.removeItem(item)
        Ui_View.Initialize(self, len(maps), len(maps[0]))
        #initialize
        #self.sizeX = len(maps)*UNIT_WIDTH
        #self.sizeY = len(maps[0])*UNIT_HEIGHT
        self.mapItem = []
        for i in range(len(maps)):
            newColumn = []
            for j in range(len(maps[i])):
                newMapUnit = MapUnit(i, j, maps[i][j])
                self.AddItem(newMapUnit)
                newColumn.append(newMapUnit)
            self.mapItem.append(newColumn)
        for i in range(len(maps)):
            for j in range(len(maps[i])):
                self.mapItem[i][j].setPos(GetPos(i, j))
        #initialization of map units
        self.soldierItem = []
        self.soldierAlive = []
        for i in range(len(units)):
            side = 0
            if (i>=side0):
                side = 1
            newSoldierUnit = SoldierUnit(i, side, units[i])
            self.AddItem(newSoldierUnit)
            self.soldierItem.append(newSoldierUnit)
            self.soldierAlive.append(True)
        self.SetSoldiers(units)
        #initialization of soldier units
        self.cursor = Cursor()
        self.AddItem(self.cursor)
        self.setMouseTracking(True)#for test
        #initialization of the cursor

    def SetSoldiers(self, units):
        "set the pos of soldiers"
        alive = map(lambda unit: (unit.life!=0), units)
        for i in range(len(units)):
            if (alive[i]!=self.soldierAlive[i] and alive[i]):
                self.scene().addItem(self.soldierItem[i])
            if (alive[i]!=self.soldierAlive[i] and not alive[i]):
                self.scene().removeItem(self.soldierItem[i])
            self.soldierAlive[i] = alive[i]
            if (self.soldierAlive[i]):
                self.soldierItem[i].setPos(GetPos(units[i].position[0],
                                                  units[i].position[1]))
                self.soldierItem[i].mapX, self.soldierItem[i].mapY = \
                                      units[i].position[0], units[i].position[1]

    #animation
    def MovingAnimation(self, idnum, route):
        "moving animation, displayed when the soldier moves"
        TIME_PER_FRAME = 1000#ms, one-step movement in a frame
        FRAMES_BEFORE_MOVE = 3
        soldier = self.soldierItem[idnum]
        #self.setPos(GetPos(route[0].x, route[0].y))
        soldier.setPos(GetPos(route[0][0], route[0][1]))
        steps = len(route)-1
        frames = steps+FRAMES_BEFORE_MOVE

        self.movTimeline = QtCore.QTimeLine(frames*TIME_PER_FRAME)
        self.movTimeline.setCurveShape(self.movTimeline.LinearCurve)
        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(soldier)
        self.animation.setTimeLine(self.movTimeline)
        for i in range(steps+1):
            #
            pos = GetPos(route[i][0], route[i][1])
            self.animation.setPosAt(float((i+FRAMES_BEFORE_MOVE))/frames, pos)
        #
        soldier.SetMapPos(route[steps][0], route[steps][1])
        self.movTimeline.start()

    def AttackingAnimation(self, selfId, targetId, damage, info = ""):
        "attack animation, displayed when the soldier launches an attack."
        TOTAL_TIME = 2000
        TIME_FOR_MOVING = 500
        TIME_WHEN_RESETING = 1960
        DIST = 0.3
        attacker = self.soldierItem[selfId]
        target = self.soldierItem[targetId]
        
        self.atkTimeline = QtCore.QTimeLine(TOTAL_TIME)
        self.atkTimeline.setCurveShape(self.atkTimeline.LinearCurve)
        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(attacker)
        self.animation.setTimeLine(self.atkTimeline)
        r = DIST/math.sqrt((attacker.mapX-target.mapX)**2+(attacker.mapY-target.mapY)**2)
        pos = attacker.GetPos()*(1-r)+target.GetPos()*r
        self.animation.setPosAt(0, attacker.GetPos())
        self.animation.setPosAt(float(TIME_FOR_MOVING)/TOTAL_TIME, pos)
        self.animation.setPosAt(float(TIME_WHEN_RESETING)/TOTAL_TIME, pos)
        self.animation.setPosAt(1, attacker.GetPos())

        text = "%+d" % damage
        if (damage==0):
            text = info
        self.label = Ui_GridLabel(text, target.mapX, target.mapY)
        self.connect(self.atkTimeline, QtCore.SIGNAL("valueChanged(qreal)"),
                     self._ShowLabel)
        #set focus
        self.atkTimeline.start()
    def _ShowLabel(self, time):
        SHOW_TIME = 0.6
        DISAP_TIME = 0.9
        if (time>=SHOW_TIME):
            self.scene().addItem(self.label)
            self.label.setPos(GetPos(self.label.mapX, self.label.mapY))
        if (time>=DISAP_TIME):
            self.scene().removeItem(self.label)

    def DiedAnimation(self, selfId):
        "displayed when a soldier dies"
        TOTAL_TIME = 2000
        TIME_PER_FRAME = 40
        soldier = self.soldierItem[selfId]

        self.dieTimeline = QtCore.QTimeLine(TOTAL_TIME)
        self.dieTimeline.setCurveShape(self.dieTimeline.LinearCurve)
        self.dieTimeline.setUpdateInterval(TIME_PER_FRAME)
        self.connect(self.dieTimeline, QtCore.SIGNAL('valueChanged(qreal)'),
                     soldier.FadeOut)
        self.dieTimeline.start()

    #def TerrainChangeAnimation(self):

    #cursor
    def TerminateAnimation(self, units = None):
        "stop the animation and rearrange the units. \
        it should be called after an naimation."
        animTimeline = [self.movTimeline, self.atkTimeline, self.dieTimeline]
        self.animation.clear()
        for timeline in animTimeline:
            timeline.stop()
            try:
                timeline.valueChanged.disconnect()
            except TypeError:
                #pass
                print "No connection!"#for test
        if (units):
            self.SetSoldiers(units)#?


