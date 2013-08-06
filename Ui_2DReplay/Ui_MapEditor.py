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
        self.usableGrid = usab;eGrid
        usableGrid.pop(ind)
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
        while (i<x):
            i += 1
            newColumn = []
            while (j<y):
                j += 1
                newColumn.append(Map_Basic(PLAIN))
            self.newMap.append(newColumn)
        #create a new map(default terrain: PLAIN)
        Ui_ReplayView.Initialize(self, self.newMap, [])
        #bug: old map unit used here!!
        #solution : add a parameter about the class

    def ChangeTerrain(self, terrain):
        "change the terrain of selected map grids"
        for i in range(len(self.newMap)):
            for j in range(len(self.newMap[i])):
                if (self.mapItem[i][j].selected):
                    self.mapItem[i][j].terrain = terrain
                    self.newMap[i][j] = Map_Basic(terrain)
                    self.mapItem[i][j].selected = False

    #def AddUnits(self, side, position):

    #need a clear function to clear the selected state?
