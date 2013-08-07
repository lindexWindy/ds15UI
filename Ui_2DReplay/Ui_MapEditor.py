#
#ver 0.1 edited at 2013-08-05-10:57 
#map editor
#Changes: init func
#need to change: terrain 'gear'
#

from Ui_2DReplayScene import *


class Ui_NewMapUnit(Ui_MapUnit):
    def __init__(self, x, y, mapGrid, parent = None):
        Ui_MapUnit.__init__(self, x, y, mapGrid, parent)
    def mousePressEvent(self, event):
        if (self.acceptEvent):
            self.selected = not self.selected
    acceptEvent = True

class Ui_NewSoldierUnit(Ui_GridUnit):
    def __init__(self, pos, side, order, parent = None):
        Ui_GridUnit.__init__(self, pos[0], pos[1], parent)
        self.side = side
        self.order = order
    #def paint(self, painter, option):
    def mousePressEvent(self, event):
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream<<self.side<<self.order
        mimedata = QtCore.QMimeData()
        mimedata.setData("&side,&order", data)

        #self.drag = QtGui.QDrag()
        self.drag = QtGui.QDrag(self)
        self.drag.setMimeData(mimedata)
        self.drag.start(QtCore.Qt.MoveAction)
        
#units of map editor



class Ui_MapEditor(Ui_ReplayView):
    def __init__(self, scene, parent = None):
        Ui_ReplayView.__init__(self, scene, parent)
        self.newMap = []

    def Initialize(self, x = 0, y = 0):
        "create a new map(default terrain: PLAIN)"
        self.newMap = []
        i = 0
        j = 0
        self.usableGrid = []
        while (i<x):
            i += 1
            newColumn = []
            while (j<y):
                j += 1
                newColumn.append(Map_Basic(PLAIN))
                self.usableGrid.append((x, y))
            self.newMap.append(newColumn)
        #create a new map(default terrain: PLAIN)
        Ui_ReplayView.Initialize(self, self.newMap, [], 0,
                                 Ui_NewMapUnit)
        self.iniUnits = [[], []]

    def ChangeTerrain(self, terrain):
        "change the terrain of selected map grids"
        for i in range(len(self.newMap)):
            for j in range(len(self.newMap[i])):
                if (self.mapItem[i][j].selected):
                    self.mapItem[i][j].terrain = terrain
                    self.newMap[i][j] = Map_Basic(terrain)
                    self.mapItem[i][j].selected = False

    def AddUnits(self, side, position = None):
        if (position==None):
            if (self.usableGrid):
                ind = 0
            else:
                pass#raise error
        else:
            if (position in self.usableGrid):
                ind = self.usableGrid.index(position)
            else:
                pass#raise error
        newUnit = Ui_NewSoldierUnit(self.usableGrid[ind],
                                    side, len(self.iniUnits[side]))
        usableGrid.pop(ind)
        newUnit.setPos(newUnit.GetPos())
        self.iniUnits[side].append(newUnit)
        return self.usableGrid[ind]
    def DelUnit(self, side):
        if (self.iniUnits[side]):
            delUnit = self.iniUnits[side][-1]
            pos = (delUnit.mapX, delUnit.mapY)
            self.iniUnits[side].pop(-1)
            self.usableGrid.append(pos)
            return pos
        else:
            pass#raise error

    def EditMapMode(self):
        if (not Ui_NewMapUnit.acceptEvent):
            Ui_NewMapUnit.acceptEvent = True
            for side in (0, 1):
                for unit in self.iniUnits[side]:
                    self.scene().removeItem(unit)
    def EditUnitMode(self):
        if (Ui_NewMapUnit.acceptEvent):
            Ui_NewMapUnit.acceptEvent = False
            for side in (0, 1):
                for unit in self.iniUnits[side]:
                    self.scene().addItem(unit)
    #function to change the mode
    #too yellow too violent

    #need a clear function to clear the selected state?

    def dragEnterEvent(self, event):
        if (event.mimeData().hasFormat("&side,&order")):
            event.accept()
        else:
            event.ignore()
    def dragMoveEvent(self, event):
        if (event.mimeData().hasFormat("&side,&order")):
            data = event.mimeData().data("&side,&order")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            side, order = 0, 0
            stream>>side>>order
            pos = GetGrid(event.scenePos().x(), event.scenePos().y())
            
            if (pos==(self.iniUnits[side][order].mapX, self.iniUnits[side][order].mapY)
                or pos in self.usableGrid):
                self.setCursor(QtCore.Qt.CloseHandCursor)
            else:
                self.setCursor(QtCore.Qt.ForbiddenCursor)
        else:
            pass
    def dropEvent(self, event):
        if (event.mimeData().hasFormat("&side,&order")):
            data = event.mimeData().data("&side,&order")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            side, order = 0, 0
            stream>>side>>order
            pos = GetGrid(event.scenePos().x(), event.scenePos().y())
            unit = self.iniUnits[side][order]

            self.setCursor(QtCore.Qt.ArrowCursor)
            if (pos in self.usableGrid):
                self.usableGrid.append((unit.mapX, unitMapY))
                unit.setMapPos(pos)
                unit.setPos(unit.GetPos())
                self.usableGrid.remove(pos)
            else:
                event.ignore()
        else:
            event.ignore()
    #drag and drop of units
