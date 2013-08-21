# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aivsai.ui'
#
# Created: Thu Aug 22 01:21:50 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AIvsAI(object):
    def setupUi(self, AIvsAI):
        AIvsAI.setObjectName(_fromUtf8("AIvsAI"))
        AIvsAI.resize(1024, 768)
        self.mapButton = QtGui.QPushButton(AIvsAI)
        self.mapButton.setGeometry(QtCore.QRect(50, 430, 141, 33))
        self.mapButton.setObjectName(_fromUtf8("mapButton"))
        self.AiButton1 = QtGui.QPushButton(AIvsAI)
        self.AiButton1.setGeometry(QtCore.QRect(50, 270, 141, 33))
        self.AiButton1.setObjectName(_fromUtf8("AiButton1"))
        self.AiButton2 = QtGui.QPushButton(AIvsAI)
        self.AiButton2.setGeometry(QtCore.QRect(50, 350, 141, 33))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AiButton2.sizePolicy().hasHeightForWidth())
        self.AiButton2.setSizePolicy(sizePolicy)
        self.AiButton2.setObjectName(_fromUtf8("AiButton2"))
        self.startButton = QtGui.QPushButton(AIvsAI)
        self.startButton.setGeometry(QtCore.QRect(791, 563, 141, 33))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.returnButton = QtGui.QPushButton(AIvsAI)
        self.returnButton.setGeometry(QtCore.QRect(791, 610, 141, 33))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))
        self.AiCombo1 = QtGui.QComboBox(AIvsAI)
        self.AiCombo1.setGeometry(QtCore.QRect(220, 273, 250, 27))
        self.AiCombo1.setObjectName(_fromUtf8("AiCombo1"))
        self.AiCombo2 = QtGui.QComboBox(AIvsAI)
        self.AiCombo2.setGeometry(QtCore.QRect(220, 353, 250, 27))
        self.AiCombo2.setObjectName(_fromUtf8("AiCombo2"))
        self.mapCombo = QtGui.QComboBox(AIvsAI)
        self.mapCombo.setGeometry(QtCore.QRect(220, 433, 250, 27))
        self.mapCombo.setObjectName(_fromUtf8("mapCombo"))
        self.roundLCD = QtGui.QLCDNumber(AIvsAI)
        self.roundLCD.setGeometry(QtCore.QRect(170, 510, 91, 41))
        self.roundLCD.setObjectName(_fromUtf8("roundLCD"))
        self.label = QtGui.QLabel(AIvsAI)
        self.label.setGeometry(QtCore.QRect(80, 520, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(AIvsAI)
        QtCore.QMetaObject.connectSlotsByName(AIvsAI)

    def retranslateUi(self, AIvsAI):
        AIvsAI.setWindowTitle(QtGui.QApplication.translate("AIvsAI", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.mapButton.setText(QtGui.QApplication.translate("AIvsAI", "载入地图", None, QtGui.QApplication.UnicodeUTF8))
        self.AiButton1.setText(QtGui.QApplication.translate("AIvsAI", "载入AI1", None, QtGui.QApplication.UnicodeUTF8))
        self.AiButton2.setText(QtGui.QApplication.translate("AIvsAI", "载入AI2", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("AIvsAI", "开始游戏", None, QtGui.QApplication.UnicodeUTF8))
        self.returnButton.setText(QtGui.QApplication.translate("AIvsAI", "返回上级", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AIvsAI", " 回合数：", None, QtGui.QApplication.UnicodeUTF8))

