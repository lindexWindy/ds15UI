#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#队式游戏主界面
from PyQt4.phonon import Phonon
from mainAnimation import *
from UiSimpleWidgets import *#BeginMenu,SingleMenu,MusicCheck
from Uibackwindow import BackWidget
from Uiteamwidget import TeamWidget
from Uiaivsai import AivsAi
import time#for test
from Uihumanvsai import HumanvsAi
#from Uimapeditor import MapEditor
from replayer import Replayer

#styleSheet = """
#QPushButton {background-image: url(image/button.jpg);}
#"""

class MainWindow(QGraphicsView):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)

		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scene1 =  QGraphicsScene()
		self.scene1.setSceneRect(self.scene1.itemsBoundingRect())
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setScene(self.scene1)
		#音乐
		self.sourceList =[]
		self.output = Phonon.AudioOutput(Phonon.MusicCategory, self)
		self.media = Phonon.MediaObject()
		Phonon.createPath(self.media, self.output)
		self.sourceList.append(Phonon.MediaSource(QString("music/music.mp3")))




		self.backWindow = QGraphicsProxyWidget()
		self.backWidget = BackWidget()
		self.backWindow.setWidget(self.backWidget)
		self.backWindow.setX(0)
		self.backWindow.setY(0)
		self.backWindow.setZValue(0)
		self.scene1.addItem(self.backWindow)
		#设置开始窗口按钮
		self.beginWindow =  QGraphicsProxyWidget()
		self.beginWidget =  BeginMenu()
		self.beginWindow.setWidget(self.beginWidget)
		self.beginWindow.setX(0)
		self.beginWindow.setY(0)
 #	   self.beginWindow.widget().setWindowOpacity(1)
		self.beginWindow.setZValue(0.5)
		self.scene1.addItem(self.beginWindow)

		#设置音乐按键
		self.musicWindow =  QGraphicsProxyWidget()
		self.musicWidget =  MusicCheck()
		self.musicWindow.setWidget(self.musicWidget)
		#写完backwidget这个位置就有意义了
		self.musicWindow.setX(self.beginWindow.widget().width()-120)
		self.musicWindow.setY(self.beginWindow.y()+20)
	#	self.musicWindow.widget().setWindowOpacity(1)
		self.musicWindow.setZValue(0.9)
#		self.musicWindow.widget()setDisabled(True)
		#设置AI对战窗口
		self.aiWindow =  QGraphicsProxyWidget()
		self.aiWidget =  AivsAi()
		self.aiWindow.setWidget(self.aiWidget)
		self.aiWindow.setX(0)
		self.aiWindow.setY(0)
		self.aiWindow.setZValue(0.5)
		self.scene1.addItem(self.musicWindow)

		#按钮控件
		self.singleWindow =  QGraphicsProxyWidget()
		self.singleWidget =  SingleMenu()
		self.singleWindow.setWidget(self.singleWidget)
		self.singleWindow.setX(0)
		self.singleWindow.setY(0)
		self.singleWindow.setZValue(0.5)
		self.scene1.addItem(self.singleWindow)

		#回放器
		self.replayWindow =  QGraphicsProxyWidget()
		self.replayWidget =  Replayer()
		self.replayWindow.setWidget(self.replayWidget)
		self.replayWindow.setX(0)
		self.replayWindow.setY(0)	
		self.replayWindow.setZValue(0.5)
		self.scene1.addItem(self.replayWindow)

		#地图编辑器
		self.mapEditWindow =  QGraphicsProxyWidget()
		self.mapWidget =  MapEditor()
		self.mapEditWindow.setWidget(self.mapWidget)
		self.mapEditWindow.setX(0)
		self.mapEditWindow.setY(0)
		self.mapEditWindow.setZValue(0.5)
		self.scene1.addItem(self.mapEditWindow)

		#人机对战
		self.humanaiWindow =  QGraphicsProxyWidget()
		self.humanaiWidget =  HumanvsAi()
		self.humanaiWindow.setX(0)
		self.humanaiWindow.setY(0)
		self.humanaiWindow.setWidget(self.humanaiWidget)
		self.humanaiWindow.setZValue(0.5)
		self.scene1.addItem(self.humanaiWindow)

		#制作团队
		self.teamWindow =  QGraphicsProxyWidget()
		self.teamWidget =  TeamWidget()
		self.teamWindow.setWidget(self.teamWidget)
		self.teamWindow.setX(0)
		self.teamWindow.setY(0)
 #	   self.teamWindow.widget().setWindowOpacity(1)
		self.teamWindow.setZValue(0.5)
		self.scene1.addItem(self.teamWindow)

 
		#登陆
		self.LogInWindow =  QGraphicsProxyWidget()
		self.logInwidget =  LogInWidget()
		self.LogInWindow.setWidget(self.logInwidget)
		self.LogInWindow.setZValue(0.5)
		self.LogInWindow.setX(0)
		self.LogInWindow.setY(0)
		self.scene1.addItem(self.LogInWindow)

		#测试赛
		self.testWindow =  QGraphicsProxyWidget()
		self.testwidget =  TestWidget()
		self.testWindow.setWidget(self.testwidget)
		self.testWindow.widget().setWindowOpacity(1)
		self.testWindow.setZValue(0.5)
		self.testWindow.setX(0)
		self.testWindow.setY(0)
		self.scene1.addItem(self.testWindow)

#		  self.beginWindow.close()
		self.aiWindow.widget().close()
		self.singleWindow.widget().close()
		self.replayWindow.widget().close()
		self.teamWindow.widget().close()
		self.mapEditWindow.widget().close()
		self.humanaiWindow.widget().close()
		self.LogInWindow.widget().close()
		self.testWindow.widget().close()

		self.windowList = [self.aiWindow, self.replayWindow, self.mapEditWindow,
							self.humanaiWindow, self.LogInWindow, self.testWindow]
#		self.menuList = [beginWindow, singleWindow]

#	self.connect(self.singleWidget.ui.replay,SIGNAL("clicked()"),self.replayWidget.GoInto)

		#设置界面背景

		#self.showFullScreen()
 #	   self.setStyleSheet(styleSheet)
	 #   file = QFile("mainStyle.qss")
	  #  file.open(QFile.ReadOnly)
	  #  styleSheet = QLatin1String(file.readAll())

	 #   self.beginWindow.widget().setStyleSheet(styleSheet)
	 #   self.singleWindow.widget().setStyleSheet(styleSheet)
	 #   for window in self.windowList:
	 #	   window.widget().setStyleSheet(styleSheet)

		#建立状态
		self.stateMachine =  QStateMachine(self)
		#main state
		self.MainState =  QState(self.stateMachine)
		#team state
		self.TeamState =  QState(self.stateMachine)
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
		#login state
		self.LogState =  QState(self.stateMachine)
		#ai state
		self.AiState = QState(self.stateMachine)
		#final state
		self.QuitState = QFinalState(self.stateMachine)

		#states和windows映射的dict
		self.stateDict = {self.MainState:self.beginWindow, self.TeamState:self.teamWindow,
						  self.ReplayState:self.replayWindow, self.MapState:self.mapEditWindow, self.AiState:self.aiWindow,
						  self.HumanaiState:self.humanaiWindow, self.LogState:self.LogInWindow,
						  self.SingleState:self.singleWindow}
		#存下上一个state
		self.preState = None


		self.trans_MainToQuit = self.MainState.addTransition(self.beginWidget.exitGameButton,
															SIGNAL("clicked()"),
															self.QuitState)
	#	self.connect(self.QuitState, SIGNAL("entered()"), self.on_quit)#for test
		#ani_MainToQuit =
#		self.tran_MainToQuit.addAnimation(ani_MainToQuit)

		self.trans_MainToSingle = self.MainState.addTransition(self.beginWindow.widget().singleGameButton,
															   SIGNAL("clicked()"),
															   self.SingleState)
		self.ani_MainToSingle = WindowAnimation(self.beginWindow, self.singleWindow)
		self.trans_MainToSingle.addAnimation(self.ani_MainToSingle)

		self.trans_SingleToMain = self.SingleState.addTransition(self.singleWidget.returnpre,
																 SIGNAL("clicked()"), self.MainState)
		self.ani_SingleToMain = WindowAnimation(self.singleWindow, self.beginWindow)
		self.trans_SingleToMain.addAnimation(self.ani_SingleToMain)

		self.trans_SingleToAi = self.SingleState.addTransition(self.singleWidget.aivsai,
															   SIGNAL("clicked()"), self.AiState)
		self.ani_SingleToAi = WindowAnimation(self.singleWindow, self.aiWindow)
		self.trans_SingleToAi.addAnimation(self.ani_SingleToAi)

		self.trans_AiToSingle = self.AiState.addTransition(self.aiWidget.returnButton, SIGNAL("clicked()"),
											 self.SingleState)
		self.ani_AiToSingle = WindowAnimation(self.aiWindow, self.singleWindow)
		self.trans_AiToSingle.addAnimation(self.ani_AiToSingle)


		self.trans_SingleToReplay = self.SingleState.addTransition(self.singleWidget.replay, SIGNAL("clicked()"),
		 			self.ReplayState)
		self.ani_SingleToReplay = WindowAnimation(self.singleWindow, self.replayWindow)
		self.trans_SingleToReplay.addAnimation(self.ani_SingleToReplay)

		self.trans_ReplayToSingle = self.ReplayState.addTransition(self.replayWidget, SIGNAL("willReturn()"),
					 self.SingleState)
		self.ani_ReplayToSingle = WindowAnimation(self.replayWindow, self.singleWindow)
		self.trans_ReplayToSingle.addAnimation(self.ani_ReplayToSingle)

		self.trans_MainToTeam = self.MainState.addTransition(self.beginWidget.teamButton,SIGNAL("clicked()"),
															  self.TeamState)
		self.trans_TeamToMain = self.TeamState.addTransition(self.teamWidget.returnButton,SIGNAL("clicked()"),
									 self.MainState)

	 #   self.trans_MapToSingle = self.MapState.addTransition(self.mapWideget.pushButton_5,SIGNAL("clicked()"),
	  #													   self.SingleState)
	   # self.trans_MapToSingle.addAnimation(WindowToMenuAnimation(mapEditWindow, singleWindow))

#		self.trans_SingleToMap = self.SingleState.addTransition(self.singleWidget.mapedit,SIGNAL("clicked()"),
 #															   self.MapState)
  #	  self.trans_SingleToMap.addAnimation(MenuToWindowAnimation(self.singleWindow, self.mapEditWindow))
#
		self.trans_SingleToHumanai = self.SingleState.addTransition(self.singleWidget.playervsai,SIGNAL("clicked()"),
  																  self.HumanaiState)
		self.ani_SingleToHumanai = WindowAnimation(self.singleWindow, self.humanaiWindow)
		self.trans_SingleToHumanai.addAnimation(self.ani_SingleToHumanai)
	

		self.trans_HumanaiToSingle = self.HumanaiState.addTransition(self.humanaiWidget, SIGNAL("willReturn()"),
 											 self.SingleState)
		self.ani_HumanaiToSingle = WindowAnimation(self.humanaiWindow, self.singleWindow)
		self.trans_HumanaiToSingle.addAnimation(self.ani_HumanaiToSingle)
#

#		self.trans_SingleToLogin = self.SingleState.addTransition(self.singleWidget.levelmode,SIGNAL("clicked()"),
 #					self.LoginState)
  #	  self.trans_SingleToLogin.addAnimation(MenuToWindowAnimation(self.singleWindow, self.LoginInWindow))
   #	 self.trans_LoginToSingle = self.LoginState.addTransition(self.LogInwidget.pushButton_2,SIGNAL("clicked()"),
	#															 self.SingleState)
	 #   self.trans_LoginToSingle.addAnimation(WindowToMenuAnimation(self.LogInWindow, self.singleWindow))

	#	self.connect(self.logInwidget,SIGNAL("login_success(QString)"),
	 #				self.LogInToTest(QString))
	 #   self.connect(self.testwidget.pushButton,SIGNAL("clicked()"),
	  #			   self.TestToLogIn)
		for state in self.stateDict.keys():
			self.connect(state, SIGNAL("entered()"), self.closeWindow)
		self.transitionList = [self.trans_MainToQuit, self.trans_MainToSingle, self.trans_SingleToMain,
							   self.trans_SingleToAi, self.trans_AiToSingle, self.trans_MainToTeam, self.trans_TeamToMain,
							   self.trans_SingleToHumanai, self.trans_HumanaiToSingle, self.trans_SingleToReplay,
							   self.trans_ReplayToSingle]
		for transition in self.transitionList:
			self.connect(transition, SIGNAL("triggered()"), self.showWindow)

		self.setAttribute(Qt.WA_DeleteOnClose)
		self.connect(self.stateMachine, SIGNAL("finished()"), self.on_quit)
		self.connect(self.musicWidget.checkBox,SIGNAL("clicked()"),
					 self.Music)
  #	  self.connect(self.replayWidget.pushButton,SIGNAL("clicked()"),
   #				  self.replayWidget.GoInto)
	#	self.connect(self.singleWidget.playervsai, SIGNAL("clicked()"),
	 #				self.humanaiWidget.initEmpty)
		self.connect(self.media,SIGNAL("aboutToFinish()"),self.continueMusic)


		self.stateMachine.setInitialState(self.MainState)
		self.stateMachine.start()


	def closeWindow(self):
		sender = self.sender()
		print sender, "hi"
		if isinstance(sender, QState):
			if sender in self.stateDict:
				if isinstance(self.preState, QState):
					self.stateDict[self.preState].widget().close()
					print "close"
			self.preState = sender

	def showWindow(self):
		sender = self.sender()
		if isinstance(sender, QAbstractTransition):
			target = sender.targetState()
			if target in self.stateDict:
				self.stateDict[target].widget().show()

	def Music(self):
		if not self.sourceList:
			QMessageBox.information(this, tr("no music files"), tr("no files to play"))
			return
		print "play1"
		#列表循环
		self.media.setQueue(self.sourceList)
		if self.media.state() == Phonon.PlayingState:
			self.media.pause()
		else:
			self.media.play()
			print "play2"

	def continueMusic(self):
		self.media.enqueue(self.sourceList)
		self.media.play()
		pass
	def closeEvent(self, event):
		if self.media.state() == Phonon.PlayingState:
			self.musicWidget.checkBox.setTristate(False)
			self.media.pause()
		self.media.stop()

	def resizeEvent(self, event):
		QGraphicsView.resizeEvent(self,event)
		self.scene1.setSceneRect(self.scene1.itemsBoundingRect())
		self.fitInView(self.scene1.sceneRect())

	#for test
	def on_quit(self):
		for ani in [self.ani_SingleToMain, self.ani_MainToSingle, self.ani_AiToSingle, self.ani_SingleToAi]:
			print ":once"
			ani.deleteLater()
		self.close()