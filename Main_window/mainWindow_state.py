#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#队式游戏主界面

from mainAnimation import *
from uiWidgets import *

class MainWindow(QGraphicsView):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        #音乐
     #   self.media = Phonon.MediaObject()
      #  self.sourceList.append(QString("music/"))
        self.pad = QGraphicsEllipseItem()
        #backwindow
        self.backWindow = QGraphicsProxyWidget(self.pad)
        self.backWidget = BackWidget()
        self.backWindow.setX(0)
        self.backWindow.setY(0)
        self.backWindow.setWidget(self.backWidget)
        self.backWindow.setZValue(0)
        self.backWindow.widget().setWindowOpacity(0)


        #设置开始窗口按钮
        self.beginWindow =  QGraphicsProxyWidget(self.pad)
        self.beginWidget =  BeginMenu()
        self.beginWindow.setWidget(self.beginWidget)
        self.beginWindow.setX(self.backWindow.x()+400)
        self.beginWindow.setY(self.backWindow.y()+200)
        self.beginWindow.widget().setWindowOpacity(1)
        self.beginWindow.setZValue(0.5)
        self.beginWindow.widget().setEnabled(True)
        #设置音乐按键
        self.musicWindow =  QGraphicsProxyWidget(self.pad)
        self.musicWidget =  ClickBottum()
        self.musicWindow.setWidget(self.musicWidget)
        self.musicWindow.setX(self.backWindow.widget().width()-120)
        self.musicWindow.setY(self.backWindow.y()+20)
        self.musicWindow.widget().setWindowOpacity(0)
        self.musicWindow.setZValue(0.9)
#        self.musicWindow.widget()setDisabled(True)
        #设置AI对战窗口
        self.aiWindow =  QGraphicsProxyWidget(self.pad)
        self.aiWidget =  AIvsAI()
        self.aiWindow.setWidget(self.aiWidget)
        self.aiWindow.setX(self.backWindow.x())
        self.aiWindow.setY(self.backWindow.y())
        self.aiWindow.widget().setWindowOpacity(0)
        self.aiWindow.setZValue(0.5)
        self.aiWindow.widget().setDisabled(True)

        #按钮控件
        self.singleWindow =  QGraphicsProxyWidget(self.pad)
        self.singleWidget =  WidgetSingle()
        self.singleWindow.setWidget(self.singleWidget)
        self.singleWindow.setX(self.backWindow.x()+400)
        self.singleWindow.setY(self.backWindow.y()+200)
        self.singleWindow.widget().setWindowOpacity(0)
        self.singleWindow.setZValue(0.5)
        self.singleWindow.widget().setDisabled(True)

        #回放器
        self.replayWindow =  QGraphicsProxyWidget(self.pad)
        self.replayWidget =  ReplayWindow()
        self.replayWindow.setWidget(self.replayWidget)
        self.replayWindow.setX(self.backWindow.x())
        self.replayWindow.setY(self.backWindow.y())
        self.replayWindow.widget().setWindowOpacity(0)
        self.replayWindow.setZValue(0.5)
        self.replayWindow.widget().setDisabled(True)

        #地图编辑器
        self.mapEditWindow =  QGraphicsProxyWidget(self.pad)
        self.mapWidget =  MapEditor()
        self.mapEditWindow.setWidget(self.mapWidget)
        self.mapEditWindow.setX(self.backWindow.x())
        self.mapEditWindow.setY(self.backWindow.y())
        self.mapEditWindow.widget().setWindowOpacity(0)
        self.mapEditWindow.setZValue(0.5)
        self.mapEditWindow.widget().setDisabled(True)

        #人机对战
        self.humanaiWindow =  QGraphicsProxyWidget(self.pad)
        self.humanaiWidget =  humanai()
        self.humanaiWindow.setX(self.backWindow.x())
        self.humanaiWindow.setY(self.backWindow.y())
        self.humanaiWindow.setWidget(self.humanaiWidget)
        self.humanaiWindow.widget().setWindowOpacity(0)
        self.humanaiWindow.setZValue(0.5)
        self.humanaiWindow.widget().setDisabled(True)

        #制作团队
        self.teamWindow =  QGraphicsProxyWidget(self.pad)
        self.teamWidget =  TeamMenu()
        self.teamWindow.setWidget(self.teamWidget)
        self.teamWindow.setX(self.backWindow.x())
        self.teamWindow.setY(self.backWindow.y())
        self.teamWindow.widget().setWindowOpacity(0)
        self.teamWindow.setZValue(0.5)

        self.teamWindow =  QGraphicsProxyWidget(self.pad)
        self.teamWideget =  ProductionTeam()
        self.teamWindow.setWidget(self.teamWideget)
        self.teamWindow.widget().setWindowOpacity(0)
        self.teamWindow.setZValue(0.5)
        self.teamWideget.setAutoFillBackground(True)
        Tpalette = self.teamWindow.palette()
        Tpalette.setBrush(QPalette.Window,
                          QBrush(Qt.black))
        self.teamWindow.setPalette(Tpalette)
        self.teamWindow.widget().setDisabled(True)
        #登陆
        self.LogInWindow =  QGraphicsProxyWidget(self.pad)
        self.logInwidget =  LogInWidget()
        self.LogInWindow.setWidget(self.logInwidget)
        self.LogInWindow.widget().setWindowOpacity(0)
        self.LogInWindow.setZValue(0.5)
        self.LogInWindow.setX(0)
        self.LogInWindow.setY(0)
        self.LogInWindow.widget().setDisabled(True)
        #测试赛
        self.testWindow =  QGraphicsProxyWidget(self.pad)
        self.testwidget =  TestWidget()
        self.testWindow.setWidget(self.testwidget)
        self.testWindow.widget().setWindowOpacity(0)
        self.testWindow.setZValue(0.5)
        self.testWindow.setX(0)
        self.testWindow.setY(0)
        self.testWindow.widget().setDisabled(True)

#          self.beginWindow.close()
      #  self.aiWindow.close()
     #   self.singleWindow.close()
       # self.replayWindow.close()
      #  self.teamWindow.close()
      #  self.teamWindow.close()
      #  self.mapEditWindow.close()
      #  self.humanaiWindow.close()
      #  self.LogInWindow.close()
      #  self.testWindow.close()

        self.windowList = [self.backWindow, self.aiWindow, self.replayWindow, self.mapEditWindow,
                           self.humanaiWindow, self.LogInWindow, self.testWindow]
#        self.menuList = [beginWindow, singleWindow]

#    self.connect(self.singleWidget.ui.replay,SIGNAL("clicked()"),self.replayWidget.GoInto)

        #设置界面背景
        self.scene =  QGraphicsScene()
        self.scene.addItem(self.pad)
        self.scene.setBackgroundBrush(QBrush(QColor(200,200,0)))
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        self.setScene(self.scene)
        self.showFullScreen()

        #建立状态
        self.stateMachine =  QStateMachine(self)
        #main state
        self.MainState =  QState(self.stateMachine)
        #team state
        self.TeamState =  QState(self.stateMachine)
      #  self.TestState =  QState(self.stateMachine)
        #replay state
        self.ReplayState =  QState(self.stateMachine)
        #web browse state
        self.WebState =  QState(self.stateMachine)
        #map edit state
        self.MapState =  QState(self.stateMachine)
        #human vs ai state
        self.HumanaiState =  QState(self.stateMachine)

        #single menu state
        self.SingleState=  QState(self.stateMachine)
      #  self.OldMenuState =  QState(self.stateMachine)
      #  self.CheckMenuState =  QState(self.stateMachine)
      #  self.TeamMenuState =  QState(self.stateMachine)
        #login state
        self.LogState =  QState(self.stateMachine)
        #ai state
        self.AiState = QState(self.stateMachine)
        #final state
        self.QuitState = QFinalState(self.stateMachine)


        self.dict = {self.MainState:self.beginWindow, self.ReplayState:self.replayWindow,
                     self.MapState:self.mapEditWindow, self.AiState:self.aiWindow,
                     self.HumanaiState:self.humanaiWindow, self.LogState:self.LogInWindow,
                     self.SingleState:self.singleWindow}

        
        self.MainState.assignProperty(self.MainState, "z", 0)
        self.MainState.assignProperty(self.beginWindow.widget(), "windowOpacity", 1)

    #    self.MainState.assignProperty(self.


        self.trans_MainToQuit = self.MainState.addTransition(self.beginWidget.exitGameButton,
                                                            SIGNAL("clicked()"),
                                                            self.QuitState)
        #ani_MainToQuit =
#        self.tran_MainToQuit.addAnimation(ani_MainToQuit)

        self.trans_MainToSingle = self.MainState.addTransition(self.beginWindow.widget().singleGameButton,
                                                               SIGNAL("clicked()"),
                                                               self.SingleState)
        self.ani_MainToSingle = MenuAnimation(self.beginWindow, self.singleWindow)
        self.trans_MainToSingle.addAnimation(self.ani_MainToSingle)

        self.trans_SingleToMain = self.SingleState.addTransition(self.singleWidget.returnpre,
                                                                 SIGNAL("clicked()"), self.MainState)
        self.ani_SingleToMain = MenuAnimation(self.singleWindow, self.beginWindow)
        self.trans_SingleToMain.addAnimation(self.ani_SingleToMain)

        self.trans_SingleToAi = self.SingleState.addTransition(self.singleWidget.aivsai,
                                                               SIGNAL("clicked()"), self.AiState)
        self.ani_SingleToAi = MenuToWindowAnimation(self.singleWindow, self.aiWindow)
        self.trans_SingleToAi.addAnimation(self.ani_SingleToAi)

      #  self.trans_AiToSingle = self.AiState.addTransition(self.aiWidget.Pre, SIGNAL("clicked()"),
          #                                   self.SingleState)
      #  self.ani_AiToSingle = WindowToMenuAnimation(self.aiWindow, self.singleWindow)
      #  self.trans_AiToSingle.addAnimation(self.ani_AiToSingle)


        #self.trans_SingleToReplay = self.SingleState.addTransition(self.singleWidget.replay, SIGNAL("clicked()"),
         #            self.ReplayState)
       # self.ani_SingleToReplay = MenuToWindowAnimation(singleWindow, replayWindow)
       # self.trans_SingleToReplay.addAnimation(self.ani_SingleToReplay)

        #self.trans_ReplayToSingle = self.ReplayState.addTransition(self.replayWidget.pushButton, SIGNAL("clicked()"),
        #             self.SingleState)
#        self.trans_ReplayToSingle.addAnimation(WindowToMenuAnimation(replayWindow, singleWindow))

 #       self.trans_BeginToTeam = self.MainState.addTransition(self.beginWidget.teamButton,SIGNAL("clicked()"),
  #                   self.TeamState)
        #不用动画这里，用信号连接
   #     self.TeamState.addTransition(self.teamWideget.pushButton,SIGNAL("clicked()"),
    #                 self.MainState)

     #   self.trans_MapToSingle = self.MapState.addTransition(self.mapWideget.pushButton_5,SIGNAL("clicked()"),
      #                                                       self.SingleState)
       # self.trans_MapToSingle.addAnimation(WindowToMenuAnimation(mapEditWindow, singleWindow))

#        self.trans_SingleToMap = self.SingleState.addTransition(self.singleWidget.mapedit,SIGNAL("clicked()"),
 #                                                               self.MapState)
  #      self.trans_SingleToMap.addAnimation(MenuToWindowAnimation(self.singleWindow, self.mapEditWindow))
#
 #       self.trans_SingleToHumanai = self.SingleState.addTransition(self.singleWidget.playervsai,SIGNAL("clicked()"),
  #                                                                  self.HumanaiState)
   #     self.trans_SingleToHumanai.addAnimation(MenuToWindowAnimation(self.singleWindow, self.humanaiWindow))


#        self.trans_HumanaiToSingle = self.HumanaiState(self.humanaiWidget.Button_back, SIGNAL("clicked()"),
 #                                                 self.SingleState)
  #      self.trans_HumanaiToSingle.addAnimation(WindowToMenuAnimation(humanaiWindow, singleWindow))
#

#        self.trans_SingleToLogin = self.SingleState.addTransition(self.singleWidget.levelmode,SIGNAL("clicked()"),
 #                    self.LoginState)
  #      self.trans_SingleToLogin.addAnimation(MenuToWindowAnimation(self.singleWindow, self.LoginInWindow))
   #     self.trans_LoginToSingle = self.LoginState.addTransition(self.LogInwidget.pushButton_2,SIGNAL("clicked()"),
    #                                                             self.SingleState)
     #   self.trans_LoginToSingle.addAnimation(WindowToMenuAnimation(self.LogInWindow, self.singleWindow))

    #    self.connect(self.logInwidget,SIGNAL("login_success(QString)"),
     #                self.LogInToTest(QString))
     #   self.connect(self.testwidget.pushButton,SIGNAL("clicked()"),
      #               self.TestToLogIn)
        for state in self.dict.keys():
            self.connect(state, SIGNAL("entered()"), self.ableWindow)
            self.connect(state, SIGNAL("exited()"), self.disWindow)
        self.connect(self.stateMachine, SIGNAL("finished()"), self, SLOT("close()"))
#        self.connect(self.musicWidget.checkBox,SIGNAL("clicked()"),
 #                    self.Music)
  #      self.connect(self.replayWidget.pushButton,SIGNAL("clicked()"),
   #                  self.replayWidget.GoInto)
    #    self.connect(self.singleWidget.playervsai, SIGNAL("clicked()"),
     #                self.humanaiWidget.initEmpty)
      #  self.connect(self.media,SIGNAL("aboutToFinish()"),self.continueMusic)

        #debug
        self.connect(self.beginWindow.widget().singleGameButton, SIGNAL("clicked()"), self.debug)
        self.stateMachine.setInitialState(self.MainState)
        self.stateMachine.start()
        print "i am ", self.beginWidget.isEnabled()
    def ableWindow(self):
        sender = self.sender()
        print sender, "hi"
        if isinstance(sender, QState):
            self.dict[sender].widget().setEnabled(True)

    def disWindow(self):
        sender = self.sender()
        print "hello"
        if isinstance(sender, QState):
            self.dict[sender].widget().setEnabled(False)

    def Music(self):
    #    if self.sourceList.isEmpty():
     #       QMessageBox.information(this, tr("no music files"), tr("no files to play"))
      #      return
        pass
#        self.media.setQueue(self.sourceList)#列表循环
#        if self.media.state() == Phonon.PlayingState:
  #          self.media.pause()
 #       else:
  #          self.media.play()

    def continueMusic(self):
    #    self.media.enqueue(self.sourceList)
     #   self.media.play()
        pass
 #   def closeEvent(self, event):
 #       if self.media.state() == Phonon.PlayingState:
  #          self.musicWidget.checkBox.setTristate(false)
   #         self.media.pause()
#        self.media.stop()

    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self,event)
       # self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def debug(self):
        print "press"
