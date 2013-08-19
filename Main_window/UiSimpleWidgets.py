# -*- coding:UTF-8 -*-
import ui_beginMenu
import ui_widgetssingle
import ui_musicCheck
from PyQt4.QtGui import QWidget

class BeginMenu(QWidget,ui_beginMenu.Ui_beginMenu):
    def __init__(self, parent = None):
        super(BeginMenu,self).__init__(parent)
        self.setupUi(self)

class WidgetSingle(QWidget,ui_widgetssingle.Ui_widgetssingle):
    def __init__(self, parent = None):
        super(WidgetSingle, self).__init__(parent)
        self.setupUi(self)

class MusicCheck(QWidget, ui_musicCheck.Ui_musicCheck):
    def __init__(self, parent = None):
        super(MusicCheck, self).__init__(parent)
        self.setupUi(self)

class BackWidget(QWidget):
    pass

#plan
class ProductionTeam(QWidget):
    pass

#plan
class TeamMenu(QWidget):
    pass


#可不可以加外部应用程序链接
class AIvsAI(QWidget):
    pass
class humanai(QWidget):
    pass
class MapEditor(QWidget):
    pass
class ReplayWindow(QWidget):
    pass

class TestWidget(QWidget):
    pass
class LogInWidget(QWidget):
    pass
