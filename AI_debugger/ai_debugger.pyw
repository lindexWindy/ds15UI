#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#AI debugger for watching two ai fighting

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import qrc_resource
from info_widget import *
#from Ai_Thread import *
from AI_2DReplayWidget import *
import socket,cPickle,time,basic
import sio

DEBUG_MODE = 1
DEFAULT_SCILENT_AI = ""#默认的ai路径,待设置


WaitForNext = QWaitCondition()
WaitForPause = QWaitCondition()

class AiThread(QThread):
    def __init__(self, lock, con, parent = None):
        super(AiThread, self).__init__(parent)

        self.lock = lock
        self.mutex = QMutex()
        self.isPaused = False#是否暂停
        self.Con = con#连续模式，连续模式下可以设置暂停
        self.Run = True#连接成功

    #每次开始游戏时，用ai路径和地图路径调用initialize以开始一个新的游戏
    def initialize(self, gameAIPath, gameMapPath):
        exception = None
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.conn.connect((sio.HOST,sio.UI_PORT))
        finally:
            if exception:
                self.conn.close()
                self.Run = False
                raise exception

            else:
                sio._sends(self.conn,(sio.AI_VS_AI, gameMapPath,gameAIPath))
                mapInfo,aiInfo,baseInfo = sio._recvs(self.conn)#add base info
                frInfo = sio._recvs(self.conn)
         #在ai_vs_ai模式里,平台并没有给用户设置自己士兵类型和英雄类型的函数
                self.emit(SIGNAL("firstRecv"),mapInfo, frInfo, aiInfo, baseInfo)

    def pause(self):
        try:
            self.mutex.lock()
            self.isPaused = True
        finally:
            self.mutex.unlock()
        if self.isPaused:
            print "i am paused"
        else:
            print "i am not paused"
    def nonPause(self):
        try:
            self.mutex.lock()
            self.isPaused = False
        finally:
            self.mutex.unlock()

    def isPaused_(self):
        try:
            self.mutex.lock()
            return self.isPaused
        finally:
            self.mutex.unlock()

    def run(self):
        #为了实现逐步暂停播放模式中用户自己下达下一回合命令和连续播放模式中
        #暂停接受数据设置的QWaitCondition全局变量
        global WaitForNext,WaitForPause
        if self.Run:
            reFlag = 0
            if self.Con and self.isPaused_():
                WaitForPause.wait(self.lock)
            if not self.Con:
                WaitForNext.wait(self.lock)
            rCommand, reInfo = sio._recvs(self.conn)
        #第一个回合单独搞出来
            self.emit(SIGNAL("reRecv"), rCommand, reInfo)
            reFlag += 1
            while reInfo.over == -1:
                #         self.conn.waitForReadyRead(-1)
                if not self.Con:
                    WaitForNext.wait(self.lock)
                if self.Con and self.isPaused_():
                #等待WaitForPause被主界面wakeall
                    print "I am waiting"
                    WaitForPause.wait(self.lock)
                    self.nonPause()
                rbInfo = sio._recvs(self.conn)
                self.emit(SIGNAL("rbRecv"),rbInfo)
            #        self.conn.waitForReadyRead(-1)
                if not self.Con:
                    WaitForNext.wait(self.lock)
                if self.Con and self.isPaused_():
                    print "i am waiting"
                    WaitForPause.wait(self.lock)
                    self.nonPause()

                rCommand,reInfo = sio._recvs(self.conn)
                self.emit(SIGNAL("reRecv"),rCommand, reInfo)
                reFlag += 1
                print "rend receive"
                print reFlag

            winner = sio._recvs(self.conn)
         #做一些界面的赢家展示替代print
            self.emit(SIGNAL("gameWinner"),winner)
            self.conn.close()
            self.emit(SIGNAL("threadEnd()"))





#调试器主界面
class ai_debugger(QMainWindow):
    def __init__(self, parent = None):
        super(ai_debugger, self).__init__(parent)

#        self.gameMode = sio.AI_VS_AI
        self.Con = 1
        self.started = False
        self.loaded_ai = []
        self.loaded_map = None
        self.lock = QReadWriteLock()#留着备用...暂时我还没有设置共同数据
        #先init这个与平台交互的线程
     #   self.pltThread = AiThread(self.lock,self)
        self.pltThread = None
#        self.replay_speed = MIN_REPLAY_SPEED
        self.ispaused = False

        #composite replay widget
        self.replayScene = QGraphicsScene()
        self.replayWindow = AiReplayWidget(self.replayScene)
        self.setCentralWidget(self.replayWindow)

        #add a dock widget to show infomations of the running AI and loaded files

        self.infoDockWidget = QDockWidget("Infos", self)
        self.infoDockWidget.setObjectName("InfoDockWidget")
        self.infoDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                            Qt.RightDockWidgetArea)
        self.infoWidget = InfoWidget(self)
        self.infoDockWidget.setWidget(self.infoWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.infoDockWidget)
        self.info_visible = self.infoDockWidget.isVisible()

        #add status bar

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)

        #creat game actions

        self.gameStartAction = self.createAction("&Start", self.startGame,
                                            "Ctrl+S","gameStart",
                                            "start game")
        #游戏暂停功能在进度条里实现,不在这里实现了(不过如果需要加入,也可以..)
      #  self.gamePauseAction = self.createAction("&Pause", self.pauseGame,
       #                                     "Ctrl+P","gamePause",
        #                                    "pause game",True)
        self.gameEndAction = self.createAction("&End", self.endGame,
                                         "Ctrl+E","gameEnd",
                                         "end game")
        self.gameLoadAction1 = self.createAction("Load &AI", self.loadAIdlg,
                                          "Ctrl+A", "loadAI",
                                          "load AI")
        self.gameLoadAction2 = self.createAction("Load &MAP", self.loadMapdlg,
                                           "Ctrl+M", "loadMap",
                                           "load MAP")
        self.gameUnloadAction = self.createAction("Unload Ais", self.unloadAI,
                                                  tip = "unload Ais")
        #creat game menu and add actions
        self.gameMenu = self.menuBar().addMenu("&Game")
        self.addActions(self.gameMenu, (self.gameStartAction,
                                  self.gameEndAction, None, self.gameLoadAction1,
                                        self.gameLoadAction2, self.gameUnloadAction))

        #creat actions and add them to config menu
        self.configMenu = self.menuBar().addMenu("&Config")
        resetAction = self.createAction("&Reset", self.reset,
                                        icon = "reset",
                                        tip = "reset all settings")
        self.configMenu.addAction(resetAction)

        modeGroup1 = QActionGroup(self)
        #还没有实现如何设置debug模式
        run_modeAction = self.createAction("Run_mode", self.setRunMode,
                                          "Ctrl+R", "modeRun", "run mode",
                                           True, "toggled(bool)")
        debug_modeAction = self.createAction("Debug_mode", self.setDebugMode,
                                            "Ctrl+D", "modeDebug", "debug mode",
                                             True, "toggled(bool)")
        modeGroup1.addAction(run_modeAction)
        modeGroup1.addAction(debug_modeAction)
        run_modeAction.setChecked(True)

        modeGroup2 = QActionGroup(self)
        continue_modeAction = self.createAction("Continuous_mode", self.setConMode,
                                               icon = "modeCon",
                                               tip = "set continuous mode",
                                               checkable = True,
                                               signal = "toggled(bool)")
        discon_modeAction = self.createAction("DisContinuous_mode", self.setDisconMode,
                                              icon = "modeDiscon",
                                              tip = "set discontinuous mode",
                                              checkable = True,
                                              signal = "toggled(bool)")
        modeGroup2.addAction(continue_modeAction)
        modeGroup2.addAction(discon_modeAction)
        continue_modeAction.setChecked(True)

        modeMenu = self.configMenu.addMenu("&Mode")
        self.addActions(modeMenu, (run_modeAction, debug_modeAction, None,
                                   continue_modeAction, discon_modeAction))

        #action group's resetable values

        self.resetableActions = ((run_modeAction, True),
                                 (debug_modeAction, False),
                                 (continue_modeAction, True),
                                 (discon_modeAction, False))
        #creat action and add it to window menu
        self.dockAction = self.createAction("(dis/en)able infos", self.setInfoWidget,
                                       tip = "enable/disable info dock-widget",
                                       checkable = True,
                                       signal = "toggled(bool)")
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.addAction(self.dockAction)
        self.dockAction.setChecked(True)
        #creat toolbars and add actions

        gameToolbar =  self.addToolBar("Game")
        self.addActions(gameToolbar, (self.gameStartAction,
                                  self.gameEndAction, self.gameLoadAction1, self.gameLoadAction2))
        configToolbar = self.addToolBar("Config")
        self.addActions(configToolbar, (run_modeAction, debug_modeAction,
                                        None, continue_modeAction,
                                        discon_modeAction, None,
                                        resetAction))


        self.connect(self.infoWidget, SIGNAL("hided()"), self.synhide)
        #to show messages
        self.connect(self.replayWindow.replayWidget, SIGNAL("unitSelected"),
                     self.infoWidget, SLOT("newUnitInfo"))
      #  self.connect(self.replayWindow.replayWidget, SIGNAL("mapGridSelected"),
       #              self.infoWidget, SLOT("newMapInfo"))

        self.connect(self.replayWindow, SIGNAL("goToRound(int, int)"), self.on_goToRound)
        print "hi11"
        #进度条到主界面的通信
        self.connect(self.replayWindow, SIGNAL("nextRound()"), self.nextRound)

        self.connect(self.replayWindow, SIGNAL("nonpauseRound()"), self.nonPauseRound)

        self.updateUi()
        self.setWindowTitle("DS15_AIDebugger")


    #wrapper function for reducing codes
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    #enable/disable actions according to the game status
    def updateUi(self):
        if len(self.loaded_ai) != 0 and self.loaded_map:
            if not self.started:
                self.gameStartAction.setEnabled(True)
              #  self.gamePauseAction.setEnabled(False)
                self.gameEndAction.setEnabled(False)
                self.gameLoadAction1.setEnabled(True)
                self.gameLoadAction2.setEnabled(True)
            else:
                self.gameStartAction.setEnabled(False)
               # self.gamePauseAction.setEnabled(True)
                self.gameEndAction.setEnabled(True)
                self.gameLoadAction1.setEnabled(False)
                self.gameLoadAction2.setEnabled(False)
        else:
            self.gameStartAction.setEnabled(False)
           # self.gamePauseAction.setEnabled(False)
            self.gameEndAction.setEnabled(False)
            self.gameLoadAction1.setEnabled(True)
            self.gameLoadAction2.setEnabled(True)
    #game operation slot
    def startGame(self):
        flag = True
        if len(self.loaded_ai) == 1:
         #加入默认的什么都不做ai
            self.loaded_ai.append(DEFAULT_SCILENT_AI)
        #开始这个线程开始交互
        self.pltThread = AiThread(self.lock, self.Con, self)
        self.connect(self.pltThread, SIGNAL("firstRecv"), self.on_firstRecv)
        try:
            self.pltThread.initialize(self.loaded_ai,self.loaded_map)
        except:
            QMessageBox.critical(self, "Connection Error",
                                 "Failed to connect to UI_PORT\n",
                                 QMessageBox.Ok, QMessageBox.NoButton)
            flag = False
        if flag:
            self.connect(self.pltThread, SIGNAL("rbRecv"), self.on_rbRecv)
            self.connect(self.pltThread, SIGNAL("reRecv"), self.on_reRecv)
            self.connect(self.pltThread, SIGNAL("gameWinner"), self.on_gameWinner)
            self.connect(self.replayWindow, SIGNAL("pauseRound()"), self.pltThread.pause)
            self.connect(self.pltThread, SIGNAL("threadEnd()"), self.on_threadEnd)

            self.started = True
            self.replayWindow.started = True
            self.replayWindow.updateUI()
            self.updateUi()

        self.connect(self.pltThread, SIGNAL("finished()"), self.pltThread,
                     SLOT("deleteLater()"))
        self.pltThread.start()
        #   def pauseGame(self):
  #      self.replayWindow.pauseGame()

    def endGame(self):
        #待实现(清空游戏缓存数据)
        #强制在游戏没有进行到胜利条件的时候结束游戏
        self.replayWindow.reset()
        self.started = False
        self.updateUi()

    #把已经选择好的的ai文件路径清空,以便修改ai文件路径
    def unloadAI(self):
        self.loaded_ai = []
        self.infoWidget.infoWidget_Game.setAiFileinfo(["",""])
        self.updateUi()

    def loadAIdlg(self):
        dir = QDir.toNativeSeparators(r"./FileAI")
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "load AI File", dir,
                                                    "AI files (%s)" % "*.py"))
        if len(self.loaded_ai) < 2 and fname:
            self.loaded_ai.append(fname)
            self.infoWidget.infoWidget_Game.setAiFileinfo(self.loaded_ai)
            self.updateUi()

    def loadMapdlg(self):
        dir = QDir.toNativeSeparators(r"./FileMap")
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "load Map File", dir,
                                                    "Map files (%s)" % "*.map"))
        if fname and fname != self.loaded_map:
            self.loaded_map = fname
            self.infoWidget.infoWidget_Game.setMapFileinfo(self.loaded_map)
            self.updateUi()

    def nextRound(self):
        global WaitForNext
        #唤醒所有在waitfornext的线程
        WaitForNext.wakeAll()

    def nonPauseRound(self):
        global WaitForPause
        #唤醒所有在waitforpause的线程

        self.pltThread.nonPause()
        WaitForPause.wakeAll()


    def on_firstRecv(self, mapInfo, frInfo, aiInfo, baseInfo):
        self.replayWindow.updateIni(basic.Begin_Info(mapInfo, baseInfo), frInfo)
        #base还没给出来?
        self.infoWidget.beginRoundInfo(frInfo)
        #这个aiInfo是什么...

    def on_rbRecv(self, rbInfo):
        self.replayWindow.updateBeg(rbInfo)
        self.infoWidget.beginRoundInfo(rbInfo)

    def on_reRecv(self, rCommand, reInfo):
        self.replayWindow.updateEnd(rCommand, reInfo)
        self.infoWidget.endRoundInfo(rCommand, reInfo)

    #进度条跳转回合信息同步(现在只同步了分数）
    def on_goToRound(self, round_, status):
        score = self.replayWindow.replayWidget.data.roundInfo[round_].score
        self.infoWidget.infoWidget_Game.setScoreinfo("%d : %d" %(score[0], score[1]))
     #   if status == 0:
      #      self.infoWidget.beginRoundInfo()
      #  else:
       #     self.infoWidget.endRoundInfo()

    #胜利展示
    def on_gameWinner(self, winner):
        QMessageBox.information(self, "Game Winner", "player %s win the game" %winner)
        #需要其他特效再加

    def on_threadEnd(self):
        self.replayWindow.started = False
        self.replayWindow.updateUI()

    def setRunMode(self):
        pass

    def setDebugMode(self):
        pass

    def setConMode(self):
        self.replayWindow.setPlayMode(1)
        #这个lock可以考虑移到AiThread类里实现
        if isinstance(self.pltThread, AiThread):
            try:
                self.pltThread.mutex.lock()
                self.pltThread.Con = 1
            finally:
                self.pltThread.mutex.unlock()
        #唤醒可能正在waitForPause的次线程，也就是说在游戏暂停时设置tForNext的次线程,跳到下一回合
            self.nextRound()
        self.Con = 1


    def setDisconMode(self):
        self.replayWindow.setPlayMode(0)
        #唤醒可能正在waitForPause的次线程，也就是说在游戏暂停时设置
        #disconMode的时候会往后跳一个状态
        if isinstance(self.pltThread, AiThread):
            try:
                self.pltThread.mutex.lock()
                self.pltThread.Con = 0
            finally:
                self.pltThread.mutex.unlock()
                self.pltThread.nonPause()
                self.nonPauseRound()
        self.Con = 0

    def reset(self):
        pass
#为了同步窗口菜单和信息栏的关闭和打开
    def synhide(self):
        self.dockAction.setChecked(False)
        self.info_visible = False
    def setInfoWidget(self):
        if (self.info_visible):
            self.infoDockWidget.close()
            self.info_visible = False
        else:
            self.infoDockWidget.show()
            self.info_visible = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ai_debugger()
    rect = QApplication.desktop().availableGeometry()
    form.resize(rect.size())
    form.setWindowIcon(QIcon(":/icon.png"))
    form.show()
    app.exec_()
