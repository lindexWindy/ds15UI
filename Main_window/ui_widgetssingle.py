# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_widgetssingle.ui'
#
# Created: Fri Oct 04 12:39:34 2013
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

class Ui_widgetssingle(object):
    def setupUi(self, widgetssingle):
        widgetssingle.setObjectName(_fromUtf8("widgetssingle"))
        widgetssingle.resize(1024, 768)
        self.frame = QtGui.QFrame(widgetssingle)
        self.frame.setGeometry(QtCore.QRect(-1, -1, 1031, 771))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.aivsai = QtGui.QPushButton(self.frame)
        self.aivsai.setGeometry(QtCore.QRect(420, 330, 140, 40))
        self.aivsai.setText(_fromUtf8(""))
        self.aivsai.setObjectName(_fromUtf8("aivsai"))
        self.playervsai = QtGui.QPushButton(self.frame)
        self.playervsai.setGeometry(QtCore.QRect(420, 400, 140, 40))
        self.playervsai.setText(_fromUtf8(""))
        self.playervsai.setObjectName(_fromUtf8("playervsai"))
        self.levelmode = QtGui.QPushButton(self.frame)
        self.levelmode.setGeometry(QtCore.QRect(420, 470, 140, 40))
        self.levelmode.setText(_fromUtf8(""))
        self.levelmode.setObjectName(_fromUtf8("levelmode"))
        self.replay = QtGui.QPushButton(self.frame)
        self.replay.setGeometry(QtCore.QRect(420, 540, 140, 40))
        self.replay.setText(_fromUtf8(""))
        self.replay.setObjectName(_fromUtf8("replay"))
        self.mapedit = QtGui.QPushButton(self.frame)
        self.mapedit.setGeometry(QtCore.QRect(420, 610, 140, 40))
        self.mapedit.setText(_fromUtf8(""))
        self.mapedit.setObjectName(_fromUtf8("mapedit"))
        self.returnpre = QtGui.QPushButton(self.frame)
        self.returnpre.setGeometry(QtCore.QRect(40, 50, 40, 40))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnpre.sizePolicy().hasHeightForWidth())
        self.returnpre.setSizePolicy(sizePolicy)
        self.returnpre.setText(_fromUtf8(""))
        self.returnpre.setObjectName(_fromUtf8("returnpre"))

        self.retranslateUi(widgetssingle)
        QtCore.QMetaObject.connectSlotsByName(widgetssingle)

    def retranslateUi(self, widgetssingle):
        widgetssingle.setWindowTitle(_translate("widgetssingle", "Form", None))

