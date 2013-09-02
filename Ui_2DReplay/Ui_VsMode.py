#
#
#

from Ui_ReplayWidgetNew import *

class Ui_OrderMenu(QtGui.QGraphicsObject):
    raise NotImplementedError



class Ui_VSModeWidget(Ui_ReplayWidget):
    def __init__(self):
        self.newInput = QtCore.QWaitConditon()
        self.mutex = QtCore.QMutex()
        raise NotImplementedError

    def Initialize(self, data, playerSide):
        raise NotImplementedError
    
#    def GameContinue(self):
#        raise NotImplementedError

#    def __PlayerRound(self):
#        raise NotImplementedError

#    def __AIRound(self):
#        raise NotImplementedError

#    def GamePause(self):

    def mousePressEvent(self, event):
        self.mutex.lock()
        Ui_ReplayWidget.mousePressEvent(self, event)
        self.newInput.wakeAll()
        self.mutex.unlock()

    def GetCommand(self):
        try:
            while True:
                self.SetCmdState(self.MOVEMENT_STATE)
                self.newInput.wait()
                if (self.input not in GetMovRange(self)):#
                    break
                movPos = self.input
                #mov anim
                #get mov pos
                self.SetCmdState(self.SET_ORDER_STATE)
                self.newInput.wait()
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
                        self.newInput.wait()
                        if (self.input==self.BREAK_FLAG):
                            break
                        avaTarget = GetAtkRange(self)
                        if (self.input in avaTarget.keys()):#
                            target = avaTarget[self.input]
                            raise CommandComplete
                elif (order==2):
                    while True:
                        self.SetCmdState(self.SELECT_SKILL_TARGET_STATE)
                        self.newInput.wait()
                        if (self.input==self.BREAK_FLAG):
                            break
                        avaTarget = GetAtkRange(self)
                        if (self.input in avaTarget.keys()):#
                            target = avaTarget[self.input]
                            raise CommandComplete
        except CommandComplete:
            cmd = Command(order, movPos, target)
            self.emit(QtCore.SIGNAL("commandComplete"), cmd)
            self.SetCmdState(self.INI_STATE)

    def ShowCmdState(self):
        raise NotImplementedError

    def SetCmdState(self):
        raise NotImplementedError

    def CmdState(self):
        raise NotImplementedError

    cmdStateChange = QtCore.pyqtSignal(int)
    pCmdState = QtCore.pyqtProperty(fget = CmdState,
                                    fset = SetCmdState,
                                    notify = cmdStateChange)
