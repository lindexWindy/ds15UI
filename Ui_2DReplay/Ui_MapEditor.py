#
#ver 0.1 edited at 2013-08-05-10:57 
#map editor
#Changes: init func
#need to change: terrain 'gear'
#

from Ui_ReplayScene import *


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

    #def ChangeTerrain(self, terrain):

    #def AddUnits(self, side, position):

    #def Clear = Initialize
