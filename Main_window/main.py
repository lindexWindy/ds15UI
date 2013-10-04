#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from mainWindow import *
import sys,time
import mainStyle

#def singleShot(main_window):
	
app = QApplication(sys.argv)
#ScreenHeight = app.desktop().availableGeometry().y()
app.setApplicationName("Mirror")

#设置stylesheet
#file = QFile("mainStyle.qss")
#file.open(QFile.ReadOnly)
#styleSheet = QLatin1String(file.readAll())
#app.setStyleSheet(styleSheet)
#style = mainStyle.Style()
#app.setStyle(style)
#设置字体
font = app.font()
font.setBold(True)
font.setLetterSpacing(QFont.PercentageSpacing, 115)
app.setFont(font)

#设置颜色
palette = app.palette()
palette.setBrush(QPalette.Active, QPalette.ButtonText, QColor(150,255,255))
palette.setBrush(QPalette.Disabled, QPalette.ButtonText, QColor(0,0,0))

#设置鼠标
cursor = QCursor(QPixmap(":cursor.png").scaled(30,30), 0, 0)
app.setOverrideCursor(cursor)

#splash
splash = QSplashScreen(QPixmap('./image/splash.png'),Qt.WindowStaysOnTopHint)


splash.show()
app.processEvents()

main_window = MainWindow()
time.sleep(2)
main_window.show()
splash.finish(main_window)
del splash

app.exec_()
