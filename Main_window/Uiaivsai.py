#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#嵌入主界面的简单ai对战界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import socket,sio
import ui_aivsai

AI_FILE_DIR = ""#ai目录路径
MAP_FILE_DIR = ""#map目录路径
class AiThread(QThread):
    def __init__(self, map, ai1, ai2, parent = None):
        super(AiThread, self).__init__(parent)
        self.map = map
        self.ai1 = ai1
        self.ai2 = ai2
    def run(self):
        #先用QProcess打开平台程序
        conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            conn.connect((sio.HOST,sio.UI_PORT))
        except:
            self.emit(SIGNAL("connectError()"))
        else:
            sio._sends(conn,(sio.AI_VS_AI, self.map ,[self.ai1, self.ai2]))

            mapInfo,aiInfo = sio._recvs(conn)

            rbInfo = sio._recvs(conn)
            rCommand,reInfo = sio._recvs(conn)
            self.emit(SIGNAL("round"))

            while reInfo.over == -1:
                rbInfo = sio._recvs(conn)
                rCommand,reInfo = sio._recvs(conn)
                self.emit(SIGNAL("round()"))

            winner = sio._recvs(conn)
            self.emit(SIGNAL("gameEnd"),winner)

	finally:
            conn.close()

class AivsAi(QWidget, ui_aivsai.Ui_AIvsAI):
    def __init__(self, parent = None):
        super(AivsAi, self).__init__(parent)
        self.setupUi(self)
        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(QPixmap("image/aiback.png")))
        self.setPalette(pal)
        self.roundLCD.display(0)

    @pyqtSlot()
    def on_startButton_clicked(self):
        self.round = 0
        self.roundLCD.display(0)
        self.ai1 = self.AiCombo1.currentText()
        self.ai2 = self.AiCombo2.currentText()
        self.map = self.mapCombo.currentText()
        if self.ai1 and self.ai2 and self.map:
            self.startGame()
        else:
            QMessageBox.critical(self, QString.fromUtf8("错误"),QString.fromUtf8("请载入ai与地图"),QMessageBox.Ok, QMessageBox.NoButton)
    @pyqtSlot()                    
    def on_AiButton1_clicked(self):
        dir = AI_FILE_DIR if AI_FILE_DIR else "."
        newAiName = unicode(QFileDialog.getOpenFileName(self, QString.fromUtf8("载入ai"),
                                                        dir, "aifile(*.py)"))
        if newAiName:
            for i in range(self.AiCombo1.count()):
                if newAiName == self.AiCombo1.itemText(i):
                    self.AiCombo1.setCurrentIndex(i)
                    return
            self.AiCombo1.addItem(newAiName)
            self.AiCombo1.setCurrentIndex(self.AiCombo1.count() - 1)
    @pyqtSlot()
    def on_AiButton2_clicked(self):
        dir = AI_FILE_DIR if AI_FILE_DIR else "."
        newAiName = unicode(QFileDialog.getOpenFileName(self,QString.fromUtf8("载入ai"),
                                                        dir, "aifile(*.py)"))
        if newAiName:
            for i in range(self.AiCombo2.count()):
                if newAiName == self.AiCombo2.itemText(i):
                    self.AiCombo2.setCurrentIndex(i)
                    return
            self.AiCombo2.addItem(newAiName)
            self.AiCombo2.setCurrentIndex(self.AiCombo2.count() - 1)
    @pyqtSlot()
    def on_mapButton_clicked(self):
        dir = MAP_FILE_DIR if MAP_FILE_DIR else "."
        newMapName = unicode(QFileDialog.getOpenFileName(self, QString.fromUtf8("载入地图"),
                                                        dir, "mapfile(*.map)"))
        if newMapName:
            for i in range(self.mapCombo.count()):
                if newMapName == self.mapCombo.itemText(i):
                    self.mapCombo.setCurrentIndex(i)
                    return
            self.mapCombo.addItem(newMapName)
            self.mapCombo.setCurrentIndex(self.mapCombo.count() - 1)

    def roundDisplay(self):
        self.round += 1
        self.roundLCD.display(self.round)


    def endGame(self, winner):
        QMessageBox.information(self, QString.fromUtf8("游戏结束"), QString.fromUtf8("ai %s 胜利" %winner))
        self.startButton.setEnabled(True)


    def connectError(self):
        QMessageBox.critical(self, QString.fromUtf8("连接错误"),QString.fromUtf8("平台连接错误"),
                             QMessageBox.Ok, QMessageBox.NoButton)
        self.startButton.setEnabled(True)

    def startGame(self):
        self.startButton.setEnabled(False)
        self.thread = AiThread(self.map, self.ai1, self.ai2, self)
        self.connect(self.thread, SIGNAL("finished()"), self.thread, SLOT("deleteLater()"))
        self.connect(self.thread, SIGNAL("gameEnd"), self.endGame)
        self.connect(self.thread, SIGNAL("connectError()"), self.connectError)
        self.connect(self.thread, SIGNAL("round()"), self.roundDisplay)
        self.thread.start()


#for test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = AivsAi()
    form.show()
    app.exec_()
