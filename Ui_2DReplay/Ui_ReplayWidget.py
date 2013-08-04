# -*- coding: utf-8 -*-
#Ver 0.3.1 edited at 2013-07-23-23:56
#Changes: animation, goto func
#Changes: data updates
#Changes: initialize
#need to change: error sended in showstatus func

#replay widget

from Ui_2DReplayScene import *


class Ui_2DReplayWidget(Ui_ReplayView):
    def __init__(self, scene, parent = None):
        Ui_ReplayView.__init__(self, scene, parent)
        self.data = None
        self.nowRound = 0
        self.status = self.BEGIN_FLAG
        self.latestRound = -1
        self.latestStatus = self.BEGIN_FLAG
        #connecting of animation
        self.animState = 0
        self.connect(self.movTimeline, QtCore.SIGNAL("finished()"),
                     self.ShowMoveAnimation)
        self.connect(self.atkTimeline, QtCore.SIGNAL("finished()"),
                     self.ShowMoveAnimation)
        self.connect(self.dieTimeline, QtCore.SIGNAL("finished()"),
                     self.ShowMoveAnimation)
        self.moveAnimEnd.connect(self.Play)
        self.begAnimEnd.connect(self.Play)
    def Initialize(self, iniInfo, begInfo):
        self.data = UiD_BattleData(iniInfo, begInfo)
        Ui_ReplayView.Initialize(self, self.data.map, self.data.iniUnits,
                                   self.data.side0SoldierNum)
        #connecting disp signals
        for column in self.mapItem:
            for grid in column:
                grid.mapGridSelected.connect(self.__callMapGridDisp)
        for unit in self.soldierItem:
            unit.soldierSelected.connect(self.__callUnitDisp)
        self.unitSelected.connect(self.__dispFun)#for test
        self.mapGridSelected.connect(self.__dispFun)#for test
        #maybe the connecting part shouldn't be here.
        self.nowRound = 0
        self.status = self.BEGIN_FLAG
        self.latestRound = 0
        self.latestStatus = self.BEGIN_FLAG
        self.ShowStatus()

    def UpdateBeginData(self, begInfo):
        if (self.data.nextRoundInfo!=None):
            pass#raise error
        self.data.nextRoundInfo = begInfo
        self.latestRound += 1
        self.latestStatus = self.BEGIN_FLAG
    def UpdateEndData(self, cmd, endInfo):
        if (self.data.nextRoundInfo==None):
            pass#raise error
        rInfo = UiD_RoundInfo(self.data.nextRoundInfo, cmd, endInfo)
        self.data.roundInfo.append(rInfo)
        self.data.nextRoundInfo = None
        self.latestStatus = self.END_FLAG

    #def GetGameInfo(self):
    #def GetTerrainInfo(self):
    #def GetSolldierInfo(self):

    def ShowStatus(self):
        self.TerminateAnimation()
        self.animState = 0
        if (self.nowRound*2+self.status>self.latestRound*2+self.latestStatus):
            pass#raise error
        units = self.__getNowUnitArray()
        self.SetSoldiers(units)

    def ShowMoveAnimation(self, state = None):
        if (state!=None):
            self.animState = state
        selfId = self.data.roundInfo[self.nowRound].idNum
        targetId = self.data.roundInfo[self.nowRound].cmdChanges.target
        move = self.data.roundInfo[self.nowRound].cmdChanges
        if (self.animState==0):
            self.MovingAnimation(selfId, move.route)
            self.animState = AFTER_MOVING
        elif (self.animState==self.AFTER_MOVING):
            pass#terrain change
            self.animState = self.AFTER_TERRAIN_CHANGE
        elif (self.animState==self.AFTER_TERRAIN_CHANGE):
            if (move.order==1):
                self.AttackingAnimation(selfId, targetId,
                                        move.damage[1], move.note[0])
                self.animState = self.AFTER_ATTACK
            elif (move.order==2):
                pass#
            else:
                self.ShowMoveAnimation(self.END_STATE)
        elif (self.animState==self.AFTER_ATTACK):
            if (move.isDead[1]):
                self.DieAnimation(self, targetId)
            elif (move.fightBack):
                self.AttackingAnimation(targetId, selfId, move.damage[0], move.note[1])
            self.animState = self.AFTER_FIGHTING_BACK
        elif (self.animState==self.AFTER_FIGHTING_BACK and move.isDead[0]):
            self.DieAnimation(selfId)
            self.animState = self.END_STATE
        else:
            #after animation
            self.TerminateAnimation()
            if (self.animState==self.END_STATE):
                self.moveAnimEnd.emit()
            self.animState = 0

    #def ShowBeginAnimation(self):

    def Play(self):
        self.nowRound += (self.nowStatus+1)/2
        self.nowStatus = (self.nowStatus+1)/2
        if (self.nowRound*2+self.status>=self.latestRound*2+self.latestStatus
            or (self.nowRound==self.latestRound and self.latestStatus==self.BEGIN_FLAG)):
            pass#raise error
        else:
            if (self.nowStatus==self.BEGIN_FLAG):
                self.ShowMoveAnimation()
            elif (self.nowStatus==self.END_FLAG):
                pass#show begin

    def GoToRound(self, r = None, flag = None):
        "stop the animation and set the round state"
        if (flag!=None):
            self.status = flaga
        if (r!=None):
            self.nowRound = r
        self.ShowStatus()

    def __callUnitDisp(self, idnum):
        self.unitSelected.emit((self.__getNowUnitArray())[idnum].__dict__)
    def __callMapGridDisp(self, x, y):
        self.mapGridSelected.emit(self.data.map[x][y].__dict__)

    def __getNowUnitArray(self):
        if (self.nowRound*2+self.status>self.latestRound*2+self.latestStatus):
            pass#raise error
        if (self.status==self.BEGIN_FLAG):
            if (self.nowRound==self.latestRound and
                self.latestStatus==self.BEGIN_FLAG):
                if (self.nowRound==0):
                    units = self.data.iniUnits
                else:
                    units = self.data.roundInfo[self.nowRound-1].endUnits
            else:
                units = self.data.roundInfo[self.nowRound].begUnits
                if (units==None):
                    if (self.nowRound==0):
                        units = self.data.iniUnits
                    else:
                        units = self.data.roundInfo[self.nowRound-1].endUnits
        elif (self.status==self.END_FLAG):
            units = self.data.roundInfo[self.nowRound].endUnits
        else:
            pass#raise error
        return units

    def __dispFun(self, dic):#for test
        print dic

    BEGIN_FLAG = 0
    END_FLAG = 1
    #flags showing the round state(at the beginning or the end)
    BEGIN_STATE = 0
    AFTER_MOVING = 1
    AFTER_TERRAIN_CHANGE = 2
    AFTER_ATTACK = 3
    AFTER_FIGHTING_BACK = 4
    PAUSE_STATE = 5
    END_STATE = 6
    #flags showing the state of the animation
    moveAnimEnd = QtCore.pyqtSignal()
    begAnimEnd = QtCore.pyqtSignal()
    #signals of animation
    unitSelected = QtCore.pyqtSignal(dict)
    mapGridSelected = QtCore.pyqtSignal(dict)
    #signals for info display




if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_2DReplayWidget(scene)
    view.setBackgroundBrush(QtGui.QColor(255, 255, 255))
    view.show()
    sys.exit(app.exec_())
    
