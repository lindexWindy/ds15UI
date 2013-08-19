# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgetssingle.ui'
#
# Created: Mon Aug 19 16:45:52 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widgetssingle(object):
    def setupUi(self, widgetssingle):
        widgetssingle.setObjectName(_fromUtf8("widgetssingle"))
        widgetssingle.resize(178, 400)
        self.playervsai = QtGui.QPushButton(widgetssingle)
        self.playervsai.setGeometry(QtCore.QRect(30, 110, 141, 31))
        self.playervsai.setObjectName(_fromUtf8("playervsai"))
        self.levelmode = QtGui.QPushButton(widgetssingle)
        self.levelmode.setGeometry(QtCore.QRect(30, 170, 141, 31))
        self.levelmode.setObjectName(_fromUtf8("levelmode"))
        self.aivsai = QtGui.QPushButton(widgetssingle)
        self.aivsai.setGeometry(QtCore.QRect(30, 50, 141, 31))
        self.aivsai.setObjectName(_fromUtf8("aivsai"))
        self.replay = QtGui.QPushButton(widgetssingle)
        self.replay.setGeometry(QtCore.QRect(30, 230, 141, 31))
        self.replay.setObjectName(_fromUtf8("replay"))
        self.mapedit = QtGui.QPushButton(widgetssingle)
        self.mapedit.setGeometry(QtCore.QRect(30, 290, 141, 31))
        self.mapedit.setObjectName(_fromUtf8("mapedit"))
        self.returnpre = QtGui.QPushButton(widgetssingle)
        self.returnpre.setGeometry(QtCore.QRect(30, 350, 141, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnpre.sizePolicy().hasHeightForWidth())
        self.returnpre.setSizePolicy(sizePolicy)
        self.returnpre.setObjectName(_fromUtf8("returnpre"))

        self.retranslateUi(widgetssingle)
        QtCore.QMetaObject.connectSlotsByName(widgetssingle)

    def retranslateUi(self, widgetssingle):
        widgetssingle.setWindowTitle(QtGui.QApplication.translate("widgetssingle", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.playervsai.setText(QtGui.QApplication.translate("widgetssingle", "人机对战", None, QtGui.QApplication.UnicodeUTF8))
        self.levelmode.setText(QtGui.QApplication.translate("widgetssingle", "闯关模式", None, QtGui.QApplication.UnicodeUTF8))
        self.aivsai.setText(QtGui.QApplication.translate("widgetssingle", "AI对战", None, QtGui.QApplication.UnicodeUTF8))
        self.replay.setText(QtGui.QApplication.translate("widgetssingle", "战争回放", None, QtGui.QApplication.UnicodeUTF8))
        self.mapedit.setText(QtGui.QApplication.translate("widgetssingle", "编辑地图", None, QtGui.QApplication.UnicodeUTF8))
        self.returnpre.setText(QtGui.QApplication.translate("widgetssingle", "返回上级", None, QtGui.QApplication.UnicodeUTF8))

