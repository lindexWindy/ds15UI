# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beginMenu.ui'
#
# Created: Mon Aug 19 22:59:29 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_beginMenu(object):
    def setupUi(self, beginMenu):
        beginMenu.setObjectName(_fromUtf8("beginMenu"))
        beginMenu.resize(263, 352)
        self.singleGameButton = QtGui.QPushButton(beginMenu)
        self.singleGameButton.setGeometry(QtCore.QRect(60, 50, 141, 31))
        self.singleGameButton.setObjectName(_fromUtf8("singleGameButton"))
        self.webGameButton = QtGui.QPushButton(beginMenu)
        self.webGameButton.setGeometry(QtCore.QRect(60, 110, 141, 31))
        self.webGameButton.setObjectName(_fromUtf8("webGameButton"))
        self.websiteButton = QtGui.QPushButton(beginMenu)
        self.websiteButton.setGeometry(QtCore.QRect(60, 170, 141, 31))
        self.websiteButton.setObjectName(_fromUtf8("websiteButton"))
        self.teamButton = QtGui.QPushButton(beginMenu)
        self.teamButton.setGeometry(QtCore.QRect(60, 230, 141, 31))
        self.teamButton.setObjectName(_fromUtf8("teamButton"))
        self.exitGameButton = QtGui.QPushButton(beginMenu)
        self.exitGameButton.setGeometry(QtCore.QRect(60, 290, 141, 31))
        self.exitGameButton.setObjectName(_fromUtf8("exitGameButton"))

        self.retranslateUi(beginMenu)
        QtCore.QMetaObject.connectSlotsByName(beginMenu)

    def retranslateUi(self, beginMenu):
        beginMenu.setWindowTitle(QtGui.QApplication.translate("beginMenu", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.singleGameButton.setText(QtGui.QApplication.translate("beginMenu", "单人游戏", None, QtGui.QApplication.UnicodeUTF8))
        self.webGameButton.setText(QtGui.QApplication.translate("beginMenu", "网络对战", None, QtGui.QApplication.UnicodeUTF8))
        self.websiteButton.setText(QtGui.QApplication.translate("beginMenu", "队式官网", None, QtGui.QApplication.UnicodeUTF8))
        self.teamButton.setText(QtGui.QApplication.translate("beginMenu", "开发组", None, QtGui.QApplication.UnicodeUTF8))
        self.exitGameButton.setText(QtGui.QApplication.translate("beginMenu", "退出游戏", None, QtGui.QApplication.UnicodeUTF8))

