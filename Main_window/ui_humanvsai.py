# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_humanvsai.ui'
#
# Created: Wed Sep  4 09:34:20 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_HumanvsAi(object):
    def setupUi(self, HumanvsAi):
        HumanvsAi.setObjectName(_fromUtf8("HumanvsAi"))
        HumanvsAi.resize(1024, 768)
        self.aiButton = QtGui.QPushButton(HumanvsAi)
        self.aiButton.setGeometry(QtCore.QRect(10, 660, 130, 29))
        self.aiButton.setObjectName(_fromUtf8("aiButton"))
        self.info_ai = QtGui.QLineEdit(HumanvsAi)
        self.info_ai.setGeometry(QtCore.QRect(150, 660, 141, 30))
        self.info_ai.setAutoFillBackground(False)
        self.info_ai.setReadOnly(True)
        self.info_ai.setObjectName(_fromUtf8("info_ai"))
        self.mapButton = QtGui.QPushButton(HumanvsAi)
        self.mapButton.setGeometry(QtCore.QRect(10, 710, 130, 29))
        self.mapButton.setObjectName(_fromUtf8("mapButton"))
        self.info_map = QtGui.QLineEdit(HumanvsAi)
        self.info_map.setGeometry(QtCore.QRect(150, 710, 141, 30))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_map.sizePolicy().hasHeightForWidth())
        self.info_map.setSizePolicy(sizePolicy)
        self.info_map.setObjectName(_fromUtf8("info_map"))
        self.verticalLayoutWidget = QtGui.QWidget(HumanvsAi)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 160, 181, 431))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(HumanvsAi)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(830, 160, 181, 431))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.startButton = QtGui.QPushButton(HumanvsAi)
        self.startButton.setGeometry(QtCore.QRect(860, 660, 130, 29))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.returnButton = QtGui.QPushButton(HumanvsAi)
        self.returnButton.setGeometry(QtCore.QRect(860, 700, 130, 29))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(HumanvsAi)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(209, 79, 601, 551))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.title = QtGui.QLabel(HumanvsAi)
        self.title.setGeometry(QtCore.QRect(380, 10, 280, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FZShuTi"))
        font.setPointSize(22)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.title.setFont(font)
        self.title.setAutoFillBackground(True)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName(_fromUtf8("title"))
        self.helpButton = QtGui.QPushButton(HumanvsAi)
        self.helpButton.setGeometry(QtCore.QRect(860, 80, 130, 29))
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.label = QtGui.QLabel(HumanvsAi)
        self.label.setGeometry(QtCore.QRect(450, 40, 141, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Amiri"))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(HumanvsAi)
        QtCore.QMetaObject.connectSlotsByName(HumanvsAi)

    def retranslateUi(self, HumanvsAi):
        HumanvsAi.setWindowTitle(QtGui.QApplication.translate("HumanvsAi", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.aiButton.setText(QtGui.QApplication.translate("HumanvsAi", "载入对战ai", None, QtGui.QApplication.UnicodeUTF8))
        self.mapButton.setText(QtGui.QApplication.translate("HumanvsAi", "载入地图", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("HumanvsAi", "开始游戏", None, QtGui.QApplication.UnicodeUTF8))
        self.returnButton.setText(QtGui.QApplication.translate("HumanvsAi", "返回上级", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("HumanvsAi", "Mirror ds15", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("HumanvsAi", "操作帮助", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HumanvsAi", "Round 0", None, QtGui.QApplication.UnicodeUTF8))

