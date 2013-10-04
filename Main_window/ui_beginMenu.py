# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_beginMenu.ui'
#
# Created: Fri Oct 04 20:26:44 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_beginMenu(object):
    def setupUi(self, beginMenu):
        beginMenu.setObjectName(_fromUtf8("beginMenu"))
        beginMenu.resize(1024, 768)
        self.frame = QtGui.QFrame(beginMenu)
        self.frame.setGeometry(QtCore.QRect(0, -1, 1031, 771))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.singleGameButton = QtGui.QPushButton(self.frame)
        self.singleGameButton.setGeometry(QtCore.QRect(460, 300, 140, 40))
        self.singleGameButton.setText(_fromUtf8(""))
        self.singleGameButton.setObjectName(_fromUtf8("singleGameButton"))
        self.webGameButton = QtGui.QPushButton(self.frame)
        self.webGameButton.setGeometry(QtCore.QRect(460, 370, 140, 40))
        self.webGameButton.setText(_fromUtf8(""))
        self.webGameButton.setObjectName(_fromUtf8("webGameButton"))
        self.websiteButton = QtGui.QPushButton(self.frame)
        self.websiteButton.setGeometry(QtCore.QRect(460, 440, 140, 40))
        self.websiteButton.setText(_fromUtf8(""))
        self.websiteButton.setObjectName(_fromUtf8("websiteButton"))
        self.teamButton = QtGui.QPushButton(self.frame)
        self.teamButton.setGeometry(QtCore.QRect(460, 510, 140, 40))
        self.teamButton.setText(_fromUtf8(""))
        self.teamButton.setObjectName(_fromUtf8("teamButton"))
        self.exitGameButton = QtGui.QPushButton(self.frame)
        self.exitGameButton.setGeometry(QtCore.QRect(460, 580, 140, 40))
        self.exitGameButton.setText(_fromUtf8(""))
        self.exitGameButton.setObjectName(_fromUtf8("exitGameButton"))

        self.retranslateUi(beginMenu)
        QtCore.QMetaObject.connectSlotsByName(beginMenu)

    def retranslateUi(self, beginMenu):
        beginMenu.setWindowTitle(_translate("beginMenu", "Form", None))

