# -*- coding: utf-8 -*-
#new version

from Ui_UnitsNew import *
from Ui_Error import Ui_Error
import sys, math
import testdata

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
        self.eventButton = event.button()
        self.eventAccept = True




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
                item.hashIndex = (item.mapX, item.mapY)
                self.unitMap[item.hashIndex].append(item)
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
        self.MouseEvent(event)
    def mouseReleaseEvent(self, event):
        self.MouseEvent(event)
    def mouseMoveEvent(self, event):
        self.MouseEvent(event)
    #transformer
    
    def MouseEvent(self, event):
        info = Ui_MouseInfo(self, event)
        self.nowPos = info.nowPos
        if (info.eventType==QtCore.QEvent.MouseButtonPress and
            info.eventButton==QtCore.Qt.LeftButton):
            self.RaiseEvent(info.nowPos, self.MOUSE_PRESS_EVENT, info)
            #handles the mouse press event
            self.dragUnit = self.RaiseEvent(info.nowPos, self.DRAG_START_EVENT, info)
            #starts a drag
        elif (info.eventType==QtCore.QEvent.MouseButtonRelease and
              (info.eventButton==QtCore.Qt.LeftButton)):
            print info.eventButton==QtCore.Qt.NoButton#for test
            if (self.dragUnit!=None):
                if (self.unitMap[info.nowPos]==[] or
                    self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.dragUnit, info))):
                    self.dragUnit.DragComplete(info)
                    self.UpdateHash(self.dragUnit.hashIndex)
                else:
                    self.dragUnit.DragFail(info)
                    raise IndexError#for test
            self.dragUnit = None
            #handles the drop event
        elif (info.eventType==QtCore.QEvent.MouseMove):
            if (self.dragUnit!=None):
                self.dragUnit.setPos(info.nowCoor-DRAG_SPOT)#handles the drag-move event
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
            if (alive[i]!=self.soldierAlive[i]):
                self.soldierItem[i].SetEnabled(alive[i])
                self.soldierAlive[i] = alive[i]
            if (self.soldierAlive[i]):
                self.soldierItem[i].SetMapPos(units[i].position[0],
                                              units[i].position[1])
                
    #animation module
    def MovingAnimation(self, idnum, route):
        "moving animation, displayed when the soldier moves"
        TIME_PER_FRAME = 1000#ms, one-step movement in a frame
        FRAMES_BEFORE_MOVE = 3
        soldier = self.soldierItem[idnum]
        steps = len(route)-1
        frames = steps+FRAMES_BEFORE_MOVE

        #movTimeline = QtCore.QTimeLine(frames*TIME_PER_FRAME)
        #movTimeline.setCurveShape(movTimeline.LinearCurve)
        #animation = QtGui.QGraphicsItemAnimation()
        #animation.setItem(soldier)
        #animation.setTimeLine(movTimeline)
        anim = Ui_Animation(soldier, "pos")
        anim.setDuration(frames*TIME_PER_FRAME)
        
        for i in range(steps+1):
            pos = GetPos(route[i][0], route[i][1])
            anim.setKeyValueAt(float((i+FRAMES_BEFORE_MOVE))/frames, pos)
        #
        #anim = {}
        #anim["timeline"] = movTimeline
        #anim["animation"] = animation
        item = []
        return anim, item

    def AttackingAnimation(self, selfId, targetId, damage, info = ""):
        "attack animation, displayed when the soldier launches an attack."
        TOTAL_TIME = 2000
        TIME_FOR_MOVING = 500
        TIME_WHEN_RESETING = 1960
        DIST = 0.3
        attacker = self.soldierItem[selfId]
        target = self.soldierItem[targetId]
        
        #atkTimeline = QtCore.QTimeLine(TOTAL_TIME)
        #atkTimeline.setCurveShape(atkTimeline.LinearCurve)
        #animation = QtCore.QGraphicsItemAnimation()
        #animation.setItem(attacker)
        #animation.setTimeLine(atkTimeline)
        r = DIST/math.sqrt((attacker.mapX-target.mapX)**2+(attacker.mapY-target.mapY)**2)
        pos = attacker.GetPos()*(1-r)+target.GetPos()*r
        atkAnim = Ui_Animation(attacker, "pos")
        atkAnim.setDuration(TOTAL_TIME)
        atkAnim.setKeyValueAt(0, attacker.GetPos())
        atkAnim.setKeyValueAt(float(TIME_FOR_MOVING)/TOTAL_TIME, pos)
        atkAnim.setKeyValueAt(float(TIME_WHEN_RESETING)/TOTAL_TIME, pos)
        atkAnim.setKeyValueAt(1, attacker.GetPos())

        text = "%+d" % damage
        if (damage==0):
            text = info
        label = Ui_GridLabel(text, target.mapX, target.mapY)
        labelAnim = Ui_Animation(label, "enability")
        labelAnim.setDuration(TOTAL_TIME)
        labelAnim.setKeyValueAt(0, False)
        labelAnim.setKeyValueAt(0.5, True)#for test
        labelAnim.setKeyValueAt(0.8, False)#for test

        anim = QtCore.QParallelAnimationGroup()
        anim.addAnimation(atkAnim)
        anim.addAnimation(labelAnim)
        #self.scene().addItem(label)
        #self.connect(atkTimeline, QtCore.SIGNAL("valueChanged(qreal)"),
        #             label.ShowLabel)
        #set focus
        item = [label]
        return anim, item

    def DiedAnimation(self, selfId):
        "displayed when a soldier dies"
        TOTAL_TIME = 2000
        TIME_PER_FRAME = 40
        soldier = self.soldierItem[selfId]

        #dieTimeline = QtCore.QTimeLine(TOTAL_TIME)
        #dieTimeline.setCurveShape(dieTimeline.LinearCurve)
        #dieTimeline.setUpdateInterval(TIME_PER_FRAME)
        #self.connect(dieTimeline, QtCore.SIGNAL('valueChanged(qreal)'),
        #             soldier.FadeOut)
        #anim = {}
        #anim["timeline"] = dieTimeline
        anim = Ui_Animation(soldier, "opacity")
        anim.setDuration(TOTAL_TIME)
        anim.setStartValue(1)
        anim.setEndValue(0)
        item = []
        return anim, item

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
        if (units!=None):
            self.SetSoldiers(units)#?




if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_ReplayView(scene)
    view.Initialize(testdata.maps, testdata.units, 3)
    #anim, item = view.MovingAnimation(0, ((0, 0), (0, 1), (1, 1), (1, 2), (1, 1)))
    #anim, item = view.AttackingAnimation(0, 1, 0, "blocked!")
    anim, item = view.DiedAnimation(3)

    view.show()
    #view.scene().addItem(item[0])
    #anim["timeline"].start()
    anim.start()
    sys.exit(app.exec_())

