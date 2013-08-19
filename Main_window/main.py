#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from mainWindow import *
import sys

app = QApplication(sys.argv)
#ScreenHeight = app.desktop().availableGeometry().y()

#设置字体
font = app.font()
font.setBold(True)
font.setLetterSpacing(QFont.PercentageSpacing, 115)
app.setFont(font)

#设置颜色
palette = app.palette()
palette.setBrush(QPalette.Active, QPalette.ButtonText, QColor(255,255,255))
palette.setBrush(QPalette.Disabled, QPalette.ButtonText, QColor(0,0,0))

#设置鼠标
cursor = QCursor(QPixmap("./image/cursor.png"))
app.setOverrideCursor(cursor)

#splash
splash = QSplashScreen()
#splash.setPixmap(QPixmap("./image/cursor.png"))
splash.show()

main_window = MainWindow()
#for window in main_window.windowList:
 #   window.setY(-ScreenHeight)
main_window.show()
splash.finish(main_window)
del splash

app.exec_()
