# -*- coding:UTF-8 -*-
import ui_beginMenu
import ui_widgetssingle
import ui_musicCheck
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class BeginMenu(QWidget,ui_beginMenu.Ui_beginMenu):
    def __init__(self, parent = None):
        super(BeginMenu,self).__init__(parent)
#        self.setAutoFillBackground(True)
        self.setupUi(self)
        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
        self.setPalette(pal)

class SingleMenu(QWidget,ui_widgetssingle.Ui_widgetssingle):
    def __init__(self, parent = None):
        super(SingleMenu, self).__init__(parent)
#        self.setAutoFillBackground(True)
        self.setupUi(self)
        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
        self.setPalette(pal)

class MusicCheck(QWidget, ui_musicCheck.Ui_musicCheck):
    def __init__(self, parent = None):
        super(MusicCheck, self).__init__(parent)
#        self.setAutoFillBackground(True)
        self.setupUi(self)
        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
        self.setPalette(pal)

#可不可以加外部应用程序链接
class AivsAi(QWidget):
    pass
class HumanvsAi(QWidget):
    pass
class MapEditor(QWidget):
    pass
class ReplayWindow(QWidget):
    pass

class TestWidget(QWidget):
    pass
class LogInWidget(QWidget):
    pass
