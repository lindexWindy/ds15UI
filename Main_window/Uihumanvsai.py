#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#人机对战界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ui_humanvsai
from Ui_2DReplay.Ui_VsMode import *
import os,sio,basic
from herotypedlg import GetHeroTypeDlg

#from AI_debugger import AiThread

try:
    _frUtf = QString.fromUtf8
except AttributeError:
    _frUtf = lambda s:s

AI_DIR = "." #默认ai目录路径
MAP_DIR = "."

WaitForCommand=QWaitCondition()

class AiThread(QThread):
    def __init__(self,parent=None):# lock, parent = None):
        super(AiThread, self).__init__(parent)

#        self.lock = lock
        self.mutex = QMutex()
#        self.Run = True#连接成功
        self.closed = False#close标识以便强制关闭线程

    #每次开始游戏时，用ai路径和地图路径调用initialize以开始一个新的游戏
    def initialize(self, gameAIPath, gameMapPath):
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.conn.connect((sio.HOST,sio.UI_PORT))
        except exception:
            self.conn.close()
#            self.Run = False
            raise exception
        else:
            sio._sends(self.conn,(sio.PLAYER_VS_AI, gameMapPath,gameAIPath))

    def isClosed(self):
        try:
            self.mutex.lock()
            return self.closed
        finally:
            self.mutex.unlock()
    def close(self):
        try:
            self.mutex.lock()
            self.closed = True
        finally:
            self.mutex.unlock()
    def run(self):
#        if self.Run:
        mapInfo,aiInfo,baseInfo = sio._recvs(self.conn)#add base info
        frInfo = sio._recvs(self.conn)
        self.emit(SIGNAL("firstRecv"),mapInfo, frInfo, aiInfo, baseInfo)
        
        rCommand, reInfo = sio._recvs(self.conn)
        self.emit(SIGNAL("reRecv"), rCommand, reInfo)
        while reInfo.over == -1 and not self.isClosed():
            rbInfo = sio._recvs(self.conn)
            if self.isClosed():
                break
            self.emit(SIGNAL("rbRecv"),rbInfo)
            rCommand,reInfo = sio._recvs(self.conn)
            if self.isClosed():
                break
            self.emit(SIGNAL("reRecv"),rCommand, reInfo)
            if not self.closed:
                winner = sio._recvs(self.conn)
                self.emit(SIGNAL("gameWinner"),winner)
        self.conn.close()

class Ui_Player(QThread):
	def __init__(self,num, parent):
            super(Ui_Player, self).__init__(parent)
            self.name = 'Thread-Player'
            self.num = num
            self.command = None
            self.lock = QReadWriteLock()
            self.parent = parent

        def initialize(self):
            self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.conn.connect((sio.HOST,sio.AI_PORT))
            except e:
                self.conn.close()
                raise e


	def GetHeroType(self,mapInfo):
            # time for player to choose herotype here!
            dialog = GetHeroTypeDlg(self.parent)
            if dialog.exec_():
                result = dialog.choice
            else:
                result = (6,6)
            return result

	def AI(self,rBeginInfo):
#			cmd=basic.Command()
			# time for player to make a command here!!
            self.emit(SIGNAL("waitforC()"))
            global WaitForCommand
            self.lock.lockForRead()
            WaitForCommand.wait(self.lock)
            return self.command

	def run(self):
		print 'ai thread called ##################################################'
		# 玩家输入名称
		aiInfo = 'Player'


		mapInfo = sio._recvs(self.conn)

		#此处向玩家展示地图,顺序有待考虑

		sio._sends(self.conn,(aiInfo,self.GetHeroType(mapInfo)))

		while True:
			rBeginInfo = sio._recvs(self.conn)
			print 'rbInfo got'
			if rBeginInfo != '|':
				sio._sends(self.conn,self.AI(rBeginInfo))
				print 'cmd sent'
			else:
				break
		self.conn.close()

class CommThread(QThread):
    def __init__(self, func, parent = None):
        super(CommTread, self).__init__(parent)
        self.func = func

    def run(self):
        self.func()

class HumanvsAi(QWidget, ui_humanvsai.Ui_HumanvsAi):
    def __init__(self, parent = None):
        super(HumanvsAi, self).__init__(parent)
        self.setupUi()

        self.aiPath = ""
        self.mapPath = ""
        self.started = False
        self.gameBegInfo = []
        self.gameEndInfo = []
        #widget
        self.replayWindow = Ui_VSModeWidget()
        self.getComm = self.replayWindow.GetCommand
        #layout
        self.verticalLayout_2.addWidget(self.replayWindow)
#        self.

        #connect
        self.connect(self.replayWindow, SIGNAL("commandComplete"), self.on_recvC)
        #other
        self.roundLabel.setWindowOpacity(0)

    def updateUi(self):
        if self.mapPath and self.aiPath and not self.started:
            self.startButton.setEnabled(True)
        else:
            self.startButton.setEnabled(False)
            
    @pyqtSlot()
    def on_aiButton_clicked(self):
        filename = QFileDialog.getOpenFileName(self, _frUtf("载入ai文件"), AI_DIR,
                                               "ai files(*.py)")
        if filename:
            self.aiPath = filename
            self.info_ai.setText(filename)
            self.updateUi()

    @pyqtSlot()
    def on_mapButton_clicked(self):
        filename = QFileDialog.getOpenFileName(self, _frUtf("载入map文件"), MAP_DIR,
                                               "map files(*.map)")
        if filename:
            self.mapPath = filename
            self.info_map.setText(filename)
            self.updateUi()

    @pyqtSlot()
    def on_startButton_clicked(self):
        #检查工作
        if not os.path.exists(r"%s" %self.aiPath):
            QMessageBox.critical(self, _frUtf("错误"), _frUtf("ai文件 %s 不存在。" %self.aiPath),
                                 QMessageBox.Ok, QMessageBox.NoButton)
            return
        if not os.path.exists(r"%s" %self.mapPath):
            QMessageBox.critical(self, _frUtf("错误"), _frUtf("map文件 %s 不存在。" %self.mapPath),
                                 QMessageBox.Ok, QMessageBox.NoButton)
            return
        #打开与平台UI_PORT连接的线程
        flag = 0
        self.aiThread = AiThread(self)
        try:
            self.aiThread.initialize(self.info_ai,self.info_map)
        except:
            flag = 1
        else:
            self.connect(self.aiThread, SIGNAL("firstRecv"), self.on_firstRecv)
            self.connect(self.aiThread, SIGNAL("rbRecv"), self.on_rbRecv)
            self.connect(self.aiThread, SIGNAL("reRecv"), self.on_reRecv)
            self.connect(self.aiThread, SIGNAL("gameWinner"), self.on_gameWinner)
#            self.connect(self.aiThread, SIGNAL("finished()"), self.replayWindow.updateUI)
            self.connect(self.aiThread, SIGNAL("finished()"), self.aiThread,
                         SLOT("deleteLater()"))

        self.playThread = Ui_Player(0, self)
        try:
            self.playTread.initialize()
        except:
            flag = 2
        else:
            #connect work
            self.connect(self.playThread, SIGNAL("waitforC()"), self.on_waitforC)

        if flag == 0:
            self.started = True
            self.updateUi()
            self.playTread.start()
            self.aiThread.start()
        elif flag == 1:
            QMessageBox.criticaltical(self, "Connection Error",
                                 "Failed to connect to UI_PORT\n",
                                 QMessageBox.Ok, QMessageBox.NoButton)
            self.aiThread.deleteLater()
        elif flag == 2:
            QMessageBox.criticaltical(self, "Connection Error",
                                      "Failed to connect to AI_PORT\n",
                                      QMessageBox.Ok, QMessageBox.NoButton)
            self.playerThread.deleteLater()

    @pyqtSlot()
    def on_helpButton_clicked(self):
        #显示帮助信息
        pass

    @pyqtSlot()
    def on_returnButton_clicked(self):
        #强制结束游戏
        pass

    def on_waitforC(self):
        #提示用户开始进行动作
        self.roundLabel.setText(_frUtf("开始操作吧!"))
        self.labelAnimation()
        self.commThread = CommThread(self, self.getComm)
        self.connect(self,commThread, SIGNAL("finished()"), self.commThread, SLOT("deleteLater()"))
        self.commThread.start()


    def on_recvC(self, cmd):
        global WaitForCommand
        try:
            self.playThread.lock.lockForWrite()
            self.playThread.command = cmd
        finally:
            self.palyThread.lock.unlock()
            WaitForCommand.wakeAll()

            
    def on_firstRecv(self, mapInfo, frInfo, aiInfo, baseInfo):
        self.replayWindow.Initialize(basic.Begin_Info(mapInfo, baseInfo), frInfo)
        self.setRoundBegInfo(frInfo)
        self.gameBegInfo.append(frInfo)
        self.roundLabel.setText("Round %d" %len(self.gameBegInfo))
        self.labelAnimation()

    def on_rbRecv(self, rbInfo):
        self.replayWindow.UpdateBeginData(rbInfo)
        self.setRoundBegInfo(rbInfo)
        self.gameBegInfo.append(rbInfo)
        self.roundLabel.setText("Round %d" %len(self.gameBegInfo))
        self.labelAnimation()

    def on_reRecv(self, rCommand, reInfo):
        self.replayWindow.UpdateEndData(rCommand, reInfo)
        self.setRoundEndInfo(rCommand, reInfo)
        self.gameEndInfo.append((rCommand,reInfo))

    def on_gameWinner(self, winner):
        QMessageBox.information(self, "Game Winner", "player %s win the game" %winner)
        #需要其他特效再加
    
    def setRoundBegInfo(self, rbInfo):
        pass
    def setRoundEndInfo(self, rCommand, reInfo):
        pass

    def labelAnimation(self):
        animation_1 = QParallelAnimationGroup(self)
        animation_1_1 = QPropertyAnimation(self.roundLabel, y)
        animation_1_1.setDuration(1500)
        animation_1_1.setStartValue(self.roundLabel.y())
        animation_1_1.setEndValue(100)
        animation_1_2 = QPropertyAnimation(self.roundLabel, opacity)
        animation_1_2.setDuaration(12000)
        animation_1_2.setStartValue(0)
        animation_1_2.setEndValue(1)
        animation_1_1.setEasingCurve(QEasingCurve.OutCubic)
        animation_1.addAnimation(animation_1_1)
        animation_1.addAnimation(animation_1_2)

        animation_2 = QParallelAnimationGroup(self)
        animation_2_1 = QPropertyAnimation(self.roundLabel, y)
        animation_2_1.setDuration(1500)
        animation_2_1.setStartValue(self.roundLabel.y())
        animation_2_1.setEndValue(40)
        animation_2_2 = QPropertyAnimation(self.roundLabel, opacity)
        animation_2_2.setDuaration(12000)
        animation_2_2.setStartValue(1)
        animation_2_2.setEndValue(0)
        animation_2_1.setEasingCurve(QEasingCurve.OutCubic)
        animation_2.addAnimation(animation_2_1)
        animation_2.addAnimation(animation_2_2)

        animation = QSequentialAnimationGroup(self)
        animation_3 = QPauseAnimation(1000)
        animation.addAnimation(animation_1)
        animation.addAnimation(animation_3)
        animation.addAnimation(animation_2)
        self.connect(animation, SIGNAL("finished()"), animation, SLOT("deleteLater()"))
        animation.start()


#test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = HumanvsAi()
    form.show()
    app.exec_()
