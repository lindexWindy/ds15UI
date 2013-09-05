#
#
#

from Ui_ReplayWidgetNew import *
import copy

CommandComplete = "command complete"



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
        Ui_2DReplayWidget.__init__(self, scene, parent)
        self.newInput = QtCore.QWaitConditon()
        self.mutex = QtCore.QMutex()
        #lock for thread
        self.cmdState = self.INIT_STATE
        self.input = None
        self.__iniPos = None
        self.__movPos = None
        self.__nowSoldier = None
        #input
        self.__prepOrder = None
        self.__prepTarget = None
        #space for storing temp cmd
        self.__dispItem = []
        #items for display

    def SetInitMap(self, maps, units = ((), ())):
        iniInfo = Begin_Info(maps, units)
        begInfo = Round_Begin_Info(None, None, units, ())
        Ui_ReplayWidget.Initialize(iniInfo, begInfo)
#        self.cmdState = self.BEGIN_STATE
        #not completed
    
    def Initialize(self, iniInfo, begInfo, cmd = None, endInfo = None):
        Ui_ReplayWidget.Initialize(self, iniInfo, begInfo[0])
        for i in range(len(begInfo)-1):
            self.UpdateEndData(cmd[i], endInfo[i])
            self.UpdateBeginData(begInfo[i+1])
        #update data
        self.cmdState = self.INIT_STATE
        self.input = None
        self.__iniPos = None
        self.__movPos = None
        self.__nowSoldier = None
        #init of input
        self.cmdStateChange.connect(self.ShowCmdState)
        #connecting....

    def UpdateBeginData(self, begInfo):
        self.nowSoldier = copy.deepcopy(begInfo.base[begInfo.id[0]][begInfo.id[1]])
        self.iniPos = self.movPos = self.nowSoldier.position
        Ui_ReplayWidget.UpdateBeginData(self, begInfo)


    def GetCommand(self):
        try:
            while True:
                self.mutex.lock()
                while True:
                    if (not self.__getMovement()):
                        break
                    if (not self.__getOrder()):
                        break
                    if (self.__prepOrder==0):
                        target = 0
                        raise CommandComplete
                    elif (self.__prepOrder==1):
                        while True:
                            if (not self.__getAtkTarget()):
                                break
                    elif (self.__prepOrder==2):
                        while True:
                            if (not self.__getSkillTarget()):
                                break
                while True:
                    if (self.__getCmdAgain()):
                        break
                self.mutex.unlock()
        except CommandComplete:
            cmd = Command(self.__prepOrder, self.__movPos, self.__prepTarget)
            self.emit(QtCore.SIGNAL("commandComplete"), cmd)
        self.SetCmdState(self.INIT_STATE)
    def __getMovement(self):
        self.SetCmdState(self.MOVEMENT_STATE)
        self.newInput.wait(self.mutex)
        if (self.input not in GetMovRange(self)):
            return False
#        nowS = self.__nowSoldier
#        mapUnit = self.data.map[nowS.position[0]][nowS.position[1]]
#        mapUnit.leave(nowS)
#        self.data.map[self.input[0]][self.input[1]].effect(nowS,
#                                                           m,
#                                                           s) ##? f**k trap!
        nowS.position = self.movPos = self.input
        return True
        #no mov anim
        #get mov pos
    def __getOrder(self):
        self.SetCmdState(self.SET_ORDER_STATE)
        self.newInput.wait(self.mutex)
        if (self.input==self.BREAK_FLAG):
            return False
        self.__prepOrder = self.input
        return True
        #get order
    def __getSkillTarget(self):
        self.SetCmdState(self.SELECT_SKILL_TARGET_STATE)
        self.newInput.wait(self.mutex)
        if (self.input==self.BREAK_FLAG):
            break
        avaTarget = GetAtkRange(self)
        if (self.input in avaTarget.keys()):#
            self.__prepTarget = avaTarget[self.input]
            raise CommandComplete
    def __getAtkTarget(self):
        self.SetCmdState(self.SELECT_ATK_TARGET_STATE)
        self.newInput.wait(self.mutex)
        if (self.input==self.BREAK_FLAG):
            return False
        avaTarget = GetAtkRange(self)
        if (self.input in avaTarget.keys()):#
            self.__prepTarget = avaTarget[self.input]
            raise CommandComplete
    def __getCmdAgain(self):
        self.__nowSoldier.position = self.__iniPos
        self.SetCmdState(INIT_STATE)
        self.newInput.wait(self.mutex)
        if (self.input==self.__iniPos):
            return True
        else:
            return False

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
            pass
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
            self.__addOrderMenu()
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
        if (oldState!=state):
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

    def __addOrderMenu(self):
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

    
    def mousePressEvent(self, event):
        self.mutex.lock()
        info = Ui_MouseInfo(self, event)
        if (info.isValid):
            self.input = info.nowPos
            self.newInput.wakeAll()
        Ui_ReplayWidget.mousePressEvent(self, event)
        self.mutex.unlock()

    def mouseMoveEvent(self, event):
        if (self.cmdState==self.MOVEMENT_STATE):
            pass
            #show route
        Ui_ReplayWidget.mouseMoveEvent(self, event)

    
