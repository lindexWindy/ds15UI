#
#
#

from Ui_ReplayWidgetNew import *
import copy

MENU_WIDTH = 60
MENU_HEIGHT = 35
class Ui_OrderSelection(QtGui.QGraphicsItem):
    def __init__(self, view, order, text, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.view = view
        self.order = order
        self.text = text
    def mousePressEvent(self, event):
        if (event.button()==QtCore.Qt.LeftButton):
            self.view.mutex.lock()
            self.view.input = self.order
            self.view.newInput.wakeAll()
            self.view.mutex.unlock()
    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             MENU_WIDTH+PEN_WIDTH, MENU_HEIGHT+PEN_WIDTH)
    def paint(self, painter, option, widget):
        raise NotImplementedError
class Ui_OrderMenu(QtGui.QGraphicsItem):
    def __init__(self, view, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        order = (1, 2, 0, Ui_VSModeWidget.BREAK_FLAG)
        text = ("attack", "skill", "standby", "back")
        for i in (0, 1, 2, 3):
            selection = Ui_OrderSelection(view, order[i], text[i])
            selection.setParentItem(self)
            selection.setPos(QtCore.QPointF(0, i*MENU_LENGTH))
    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             MENU_WIDTH+PEN_WIDTH, MENU_HEIGHT*4+PEN_WIDTH)
    def paint(self, painter, option, widget):
        raise NotImplementedError

#class Ui_TempSoldier(Ui_SoldierUnit):
#    raise NotImplementedError



class Ui_VSModeWidget(Ui_2DReplayWidget):
    def __init__(self, scene, parent = None):
        self.newInput = QtCore.QWaitConditon()
        self.mutex = QtCore.QMutex()

        self.cmdState = self.INIT_STATE
        self.movPos = None
        self.nowSoldier = None
        raise NotImplementedError

    def SetInitMap(self, maps, units = ((), ())):
        iniInfo = Begin_Info(maps, units)
        begInfo = Round_Begin_Info(None, None, units, ())
        Ui_ReplayWidget.Initialize(iniInfo, begInfo)
    
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
            #how to exit the novement state?
            while True:
                self.mutex.lock()
                self.SetCmdState(self.MOVEMENT_STATE)
                self.newInput.wait(self.mutex)
                if (self.input not in GetMovRange(self)):#
                    continue#
                self.movPos = self.input
                raise NotImplementedError
                #self.nowSoldier
                #no mov anim
                #get mov pos
                self.SetCmdState(self.SET_ORDER_STATE)
                self.newInput.wait(self.mutex)
                if (self.input==self.BREAK_FLAG):
                    continue#
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

    def GetAtkTarget(self):
        avalUnits = {}
        units = self.__getNowUnitArray()
        for i in units.keys():
            if (HammDist(self.nowSoldier.position,
                         units[i].position)<=self.nowSoldier.attack_range
                and i[0]!=self.data.roundInfo[self.nowRound].idNum[0]):
                avalUnits[units[i].position] = i
        return avalUnits
    def GetSkillTarget(self):
        raise NotImplementedError

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
#            self.tempSoldier = Ui_TempSoldier(self.nowPos[0], self.nowPos[1])
            self.scene().addItem(self.tempSoldier)
            self.__AddOrderMenu()
            self.setEnabled(False)
        elif (state==self.SELECT_ATK_TARGET_STATE):
#            self.tempSoldier = Ui_TempSoldier(self.nowPos[0], self.nowPos[1])
            self.scene().addItem(self.tempSoldier)
#            for item in self.scene().items():
#                if (HammDist(self.nowPos, (item.mapX, item.mapY))<=self.nowSoldier.attack_range):
#                    item.selected = True
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

    INIT_STATE = 0
    MOVEMENT_STATE = 1
    SET_ORDER_STATE = 2
    SELECT_ATK_TARGET_STATE = 3
    SELECT_SKILL_TARGET_STATE = 4
    BEGIN_STATE = 5##
    BREAK_FLAG = -1

    cmdStateChange = QtCore.pyqtSignal(int, int)
    pCmdState = QtCore.pyqtProperty(int, fget = CmdState,
                                    fset = SetCmdState,
                                    notify = cmdStateChange)

    def __AddOrderMenu(self):
        x, y = self.nowPos
        sizeX, sizeY = self.mapSize
        point = QtCore.QPointF(UNIT_WIDTH/2, UNIT_LENGTH/2)
        if (x==sizeX-1):
            point -= QtCore.QPointF(MENU_WIDTH, 0)
        if (y==sizeY-1):
            point -= QtCore.QPointF(0, MENU_HEIGHT)
        if (sizeX==1 or sizeY==1):
            point = QtCore.QPointF(UNIT_WIDTH-MENU_WIDTH, 0)
        self.menu = Ui_OrderMenu(self)
        self.scene().addItem(self.menu)
        self.menu.setPos(GetPos(x, y)+point)

    
