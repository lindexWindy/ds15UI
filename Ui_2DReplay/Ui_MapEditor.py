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
        self.selected = not self.selected

class Ui_NewSoldierUnit(Ui_GridUnit):
    def __init__(self, usableGrid, ind = 0, parent = None):
        Ui_GridUnit.__init__(self,
                             usableGrid[ind][0], usableGrid[ind][1], parent)
        self.usableGrid = usableGrid
        usableGrid.pop(ind)
    #def paint(self, painter, option):
    #def mouseDragEvent(self, event):
        
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
        newUnit = Ui_NewMapUnit(self.usableGrid, ind)
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

    #need a clear function to clear the selected state?
