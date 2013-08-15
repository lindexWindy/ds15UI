# -*- coding: utf-8 -*-
#
#ver 0.1 edited at 2013-08-12-08:27 
#map editor
#Changes: completed
#need to change: terrain 'gear', drag-and-drop operation
#

from Ui_2DReplayScene import *

class Ui_NewMapUnit(Ui_MapUnit):
    def __init__(self, x, y, mapGrid, parent = None):
        Ui_MapUnit.__init__(self, x, y, mapGrid, parent)
    def mousePressEvent(self, event):
        if (self.acceptEvent):
            print "yes"#for test
            print self.mapX, self.mapY#for test
            self.selected = not self.selected
    acceptEvent = True

class Ui_NewSoldierUnit(Ui_GridUnit):
    def __init__(self, pos, side, order, parent = None):
        Ui_GridUnit.__init__(self, pos[0], pos[1], parent)
        self.side = side
        self.order = order
        self.setAcceptDrops(True)
    def paint(self, painter, option, widget):
        painter.drawRect(10, 10, 50, 50)#for test
    def mousePressEvent(self, event):
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream<<QtCore.QPoint(self.side, self.order)
        mimedata = QtCore.QMimeData()
        mimedata.setData("&side,&order", data)

        drag = QtGui.QDrag(event.widget())
        print self.mapX, self.mapY#for test
        print event.pos()#for test
        drag.setMimeData(mimedata)
        drag.exec_()
        
#units of map editor



class Ui_MapEditor(Ui_ReplayView):
    "display widget in map editor. \
    data: \
    newMap : Map \
    iniUnits : array of Units"
    def __init__(self, scene, parent = None):
        Ui_ReplayView.__init__(self, scene, parent)
        self.newMap = []
        self.usableGrid = []
        self.iniUnits = [[], []]
        self.setAcceptDrops(True)

    def Initialize(self, x = 0, y = 0):
        "Initialize(int x = 0, int y = 0) -> void \
        create a new map(default terrain: PLAIN). \
        x and y is the size of the map. "
        self.newMap = []
        i = 0
        self.usableGrid = []
        while (i<x):
            j = 0
            newColumn = []
            while (j<y):
                newColumn.append(Map_Basic(PLAIN))
                self.usableGrid.append((i, j))
                j += 1
            self.newMap.append(newColumn)
            i += 1
        Ui_ReplayView.Initialize(self, self.newMap, [], 0,
                                 Ui_NewMapUnit)
        self.iniUnits = [[], []]

    def ChangeTerrain(self, terrain):
        "ChangeTerrain(enum TERRAIN terrain) -> void \
        change the terrain of selected map grids "
        for i in range(len(self.newMap)):
            for j in range(len(self.newMap[i])):
                if (self.mapItem[i][j].selected):
                    self.mapItem[i][j].terrain = terrain
                    self.newMap[i][j] = Map_Basic(terrain)
                    self.mapItem[i][j].selected = False
        self.scene().update()

    def AddUnit(self, side, position = None):
        "AddUnit(enum(0, 1) side, Coord. position = None) -> Coord. newPos \
        add a new unit to a certain side returning the position it will placed at. \
        position indicates where the new unit should be set. \
        if it is None, a valid and random position will be distributed. \
        error will be raised if the position is invalid."
        if (position==None):
            if (self.usableGrid):
                ind = 0
            else:
                raise Ui_Error, ("AddUnitError_0",
                                 ("class Ui_MapEditor", "func AddUnit"),
                                 "无合法的格点。")
        else:
            if (position in self.usableGrid):
                ind = self.usableGrid.index(position)
            else:
                raise Ui_Error, ("AddUnitError_1",
                                 ("class Ui_MapEditor", "func AddUnit"),
                                 "所选格点不合法，或已有单位存在。")
        newUnit = Ui_NewSoldierUnit(self.usableGrid[ind],
                                    side, len(self.iniUnits[side]))
        nowpos = self.usableGrid.pop(ind)
        newUnit.setPos(newUnit.GetPos())
        self.scene().addItem(newUnit)
        self.iniUnits[side].append(newUnit)
        #self.scene().update()
        return nowpos
    def DelUnit(self, side):
        "DelUnit(enum(0, 1) side) -> Coord. pos \
        delete the last unit of a certain side returning the position it was placed at. \
        error will be raised if no units is in this side."
        if (self.iniUnits[side]):
            delUnit = self.iniUnits[side].pop(-1)
            self.scene().removeItem(delUnit)
            pos = (delUnit.mapX, delUnit.mapY)
            self.usableGrid.append(pos)
            #self.scene().update()
            return pos
        else:
            raise Ui_Error, ("DelUnitError",
                             ("class Ui_MapEditor", "func DelUnit"),
                             "无可删除的单位。")

    def EditMapMode(self):
        "EditMapMode() -> void \
        set the widget in the map-editing mode."
        if (not Ui_NewMapUnit.acceptEvent):
            Ui_NewMapUnit.acceptEvent = True
            for side in (0, 1):
                for unit in self.iniUnits[side]:
                    self.scene().removeItem(unit)
    def EditUnitMode(self):
        "EditUnitMode() -> void \
        set the widget in the unit-placing mode."
        if (Ui_NewMapUnit.acceptEvent):
            Ui_NewMapUnit.acceptEvent = False
            for side in (0, 1):
                for unit in self.iniUnits[side]:
                    self.scene().addItem(unit)
    #function to change the mode
    #too yellow too violent

    #need a clear function to clear the selected state?

    #def dragEnterEvent(self, event):
        #if (event.mimeData().hasFormat("&side,&order")):
            #event.accept()
        #else:
            #event.ignore()
    def dragMoveEvent(self, event):
        if (event.mimeData().hasFormat("&side,&order")):
            data = event.mimeData().data("&side,&order")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            point = QtCore.QPoint()
            stream>>point
            side, order = point.x(), point.y()
            scenePos = self.mapToScene(event.pos())
            pos = GetGrid(scenePos.x(), scenePos.y())
            print "lllllll"#for test
            
            if (pos==(self.iniUnits[side][order].mapX, self.iniUnits[side][order].mapY)
                or pos in self.usableGrid):
                pass
                #self.setCursor(QtCore.Qt.CloseHandCursor)
            else:
                self.setCursor(QtCore.Qt.ForbiddenCursor)
        else:
            pass
    def dropEvent(self, event):
        print "fkjasdf"#for test
        if (event.mimeData().hasFormat("&side,&order")):
            data = event.mimeData().data("&side,&order")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            point = QtCore.QPoint()
            stream>>point
            side, order = point.x(), point.y()
            scenePos = self.mapToScene(event.pos())
            pos = GetGrid(scenePos.x(), scenePos.y())
            unit = self.iniUnits[side][order]

            self.setCursor(QtCore.Qt.ArrowCursor)
            if (pos in self.usableGrid):
                self.usableGrid.append((unit.mapX, unit.mapY))
                unit.SetMapPos(pos[0], pos[1])
                unit.setPos(unit.GetPos())
                self.usableGrid.remove(pos)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
    #drag and drop of units
