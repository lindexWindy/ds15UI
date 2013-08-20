# -*- coding: utf-8 -*-
#Ver 0.3.1 edited at 2013-07-23-23:56
#Changes: animation, goto func
#Changes: data updates
#Changes: initialize
#need to change: error sended in showstatus func

#replay widget

from Ui_2DReplaySceneNew import *


class Ui_2DReplayWidget(Ui_ReplayView):
    def __init__(self, scene, parent = None):
        Ui_ReplayView.__init__(self, scene, parent)
        self.data = None
        self.nowRound = 0
        self.status = self.BEGIN_FLAG
        self.latestRound = -1
        self.latestStatus = self.BEGIN_FLAG
        self.anim = None
        self.additionItem = []
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
        rInfo = UiD_RoundInfo(self.data.nextRoundInfo, cmd, endInfo, self.data.map)
        self.data.roundInfo.append(rInfo)
        self.data.nextRoundInfo = None
        self.latestStatus = self.END_FLAG

    #def GetGameInfo(self):
    #def GetTerrainInfo(self):
    #def GetSolldierInfo(self):

    def ShowStatus(self):
        self.__TerminateAnimation()
        self.animState = 0
        if (self.nowRound*2+self.status>self.latestRound*2+self.latestStatus):
            pass#raise error
        units = self.__getNowUnitArray()
        self.SetSoldiers(units)

    def ShowMoveAnimation(self, state = None):
        #check
        if (self.status==self.END_FLAG):
            return
        self.ShowStatus()
        try:
            cmd = self.data.roundInfo[self.nowRound].cmdChanges
        except IndexError:
            return#raise error?
        #initialize
        self.status = self.END_FLAG
        self.animState = self.ANIM_RUNNING
        self.anim = QtCore.QSequentialAnimationGroup()
        self.additionItem = []
        #move
        anim, item = self.MovingAnimation(cmd.idNum, self.route)
        self.anim.addAnimation(anim)
        self.additionItem.extend(item)
        #terrain changes
        #
        if (cmd.order==1):#attack
            anim, item = self.AttackingAnimation(cmd.idNum, cmd.target,
                                                 cmd.damage[1], cmd.note[1])
            self.anim.addAnimation(anim)
            self.additionItem.extend(item)
            if (cmd.isDead[1]):#target died
                anim, item = self.DiedAnimation(cmd.target)
                self.anim.addAnimation(anim)
                self.additionItem.extend(item)
            elif (cmd.fightBack):#target fights back
                anim, item = self.AttackingAnimation(cmd.target, cmd.idNum,
                                                     cmd.damage[0], cmd.damage[1])
                self.anim.addAnimation(anim)
                self.additionItem.extend(item)
                if (cmd.isDead[0]):#attacker dies
                    anim, item = self.DiedAnimation(cmd.idNum)
                    self.anim.addAnimation(anim)
                    self.additionItem.extend(item)
        #some other prepararion
        for item in self.additionItem:
            self.scene().addItem(item)
            item.SetEnabled(False)#set them invisible
        self.connect(self.anim, SIGNAL("finished()"), self.ShowStatus)
        self.connect(self.anim, SIGNAL("finished()"), self.moveAnimEnd)

        self.anim.start()

    def __TerminateAnimation(self):
        if (self.anim!=None):
            self.anim.stop()
        self.animState = ANIM_STOP
        for item in self.additonItem:
            self.scene().removeItem(item)
        self.additionItem = []

                
        

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
            self.status = flag
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
    
