#
#
#

from Ui_ReplayWidgetNew import *
import copy

class Ui_OrderMenu(QtGui.QGraphicsObject):
    raise NotImplementedError

class Ui_TempSoldier(Ui_GridUnit):
    raise NotImplementedError



class Ui_VSModeWidget(Ui_ReplayWidget):
    def __init__(self):
        self.newInput = QtCore.QWaitConditon()
        self.mutex = QtCore.QMutex()

        self.cmdState = self.INIT_STATE
        self.movPos = None
        self.nowSoldier = None
        raise NotImplementedError

    def Initialize(self, iniInfo, begInfo, cmd = None, endInfo = None):
        Ui_ReplayWidget.Initialize(self, iniInfo, begInfo[0])
        for i in range(len(begInfo)-1):
            self.UpdateEndData(cmd[i], endInfo[i])
            self.UpdateBeginData(begInfo[i+1])
        #update data
        self.GoToRound(self.latestRound, self.latestStatus)
        self.cmdState = self.INIT_STATE
        self.movPos = None
        #
        raise NotImplementedError
        #connecting....

    def UpdateBeginData(self, begInfo):
        self.nowSoldier = copy.deepcopy(begInfo.base[begInfo.id[0]][begInfo.id[1]])
        Ui_ReplayWidget.UpdateBeginData(self, begInfo)
        
#    def GameContinue(self):
#        raise NotImplementedError

#    def __PlayerRound(self):
#        raise NotImplementedError

#    def __AIRound(self):
#        raise NotImplementedError

#    def GamePause(self):

    def mousePressEvent(self, event):
        self.mutex.lock()
        info = Ui_MouseInfo(self, event)
        if (info.isValid):
            self.input = info.nowPos
            self.newInput.wakeAll()
        Ui_ReplayWidget.mousePressEvent(self, event)
        self.mutex.unlock()

    def GetCommand(self):
        try:
            while True:
                self.mutex.lock()
                self.SetCmdState(self.MOVEMENT_STATE)
                self.newInput.wait(self.mutex)
                if (self.input not in GetMovRange(self)):#
                    break
                self.movPos = self.input
                raise NotImplementedError
                #self.nowSoldier
                #no mov anim
                #get mov pos
                self.SetCmdState(self.SET_ORDER_STATE)
                self.newInput.wait(self.mutex)
                if (self.input==self.BREAK_FLAG):
                    break
                order = self.input
                #get order
                if (order==0):
                    target = 0
                    raise CommandComplete
                elif (order==1):
                    while True:
                        self.SetCmdState(self.SELECT_ATK_TARGET_STATE)
                        self.newInput.wait(self.mutex)
                        if (self.input==self.BREAK_FLAG):
                            break
                        avaTarget = GetAtkRange(self)
                        if (self.input in avaTarget.keys()):#
                            target = avaTarget[self.input]
                            raise CommandComplete
                elif (order==2):
                    while True:
                        self.SetCmdState(self.SELECT_SKILL_TARGET_STATE)
                        self.newInput.wait(self.mutex)
                        if (self.input==self.BREAK_FLAG):
                            break
                        avaTarget = GetAtkRange(self)
                        if (self.input in avaTarget.keys()):#
                            target = avaTarget[self.input]
                            raise CommandComplete
                self.mutex.unlock()
        except CommandComplete:
            cmd = Command(order, self.movPos, target)
            self.emit(QtCore.SIGNAL("commandComplete"), cmd)
            self.SetCmdState(self.INIT_STATE)

    def ShowCmdState(self, oldState, state):
        for item in self.scene().items():
            item.selected = False
        if (oldState==self.INIT_STATE):
            pass
        elif (oldState==self.MOVEMENT_STATE):
            raise NotImplementedError
        elif (oldState==self.SET_ORDER_STATE):
            self.scene().removeItem(self.menu)
            del self.menu
            self.scene().removeItem(self.tempSoldier)
            del self.tempSoldier
            self.setEnabled(False)
        elif (oldState==self.SELECT_ATK_TARGET_STATE):
            self.scene().removeItem(self.tempSoldier)
            del self.tempSoldier
        elif (oldState==self.SELECT_SKILL_TARGET_STATE):
            self.scene().removeItem(self.tempSoldier)
            del self.tempSoldier
        else:
            raise TypeError
        
        if (state==self.INIT_STATE):
            pass
        elif (state==self.MOVEMENT_STATE):
            movRng = self.GetMovRange()
            for item in self.scene().items():
                if ((item.mapX, item.mapY) in movRng):
                    item.selected = True#type?
                    raise NotImplementedError
        elif (state==self.SET_ORDER_STATE):
            self.tempSoldier = Ui_TempSoldier(self.nowPos[0], self.nowPos[1])
            self.scene().addItem(self.tempSoldier)
            self.__AddOrderMenu()
            self.setEnabled(False)
        elif (state==self.SELECT_ATK_TARGET_STATE):
            self.tempSoldier = Ui_TempSoldier(self.nowPos[0], self.nowPos[1])
            self.scene().addItem(self.tempSoldier)
            for item in self.scene().items():
                if (HammDist(self.nowPos, (item.mapX, item.mapY))<=self.nowSoldier.attack_range):
                    item.selected = True
        elif (state==self.SELECT_SKILL_TARGET_STATE):
            self.tempSoldier = Ui_TempSoldier(self.nowPos[0], self.nowPos[1])
            self.scene().addItem(self.tempSoldier)
            raise NotImplementedError
        else:
            raise TypeError
        self.scene().update()

    def SetCmdState(self, state):
        oldState = self.cmdState
        self.cmdState = state
        cmdStateChange.emit(oldState, state)

    def CmdState(self):
        return self.cmdState

    cmdStateChange = QtCore.pyqtSignal(int, int)
    pCmdState = QtCore.pyqtProperty(fget = CmdState,
                                    fset = SetCmdState,
                                    notify = cmdStateChange)

    def __AddOrderMenu(self):
        raise NotImplementedError
