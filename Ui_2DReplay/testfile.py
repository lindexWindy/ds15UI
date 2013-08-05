# -*- coding: UTF-8 -*-

from Ui_ReplayWidget import *
from testdata import *


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_2DReplayWidget(scene)
    view.setBackgroundBrush(QtGui.QColor(0, 0, 0))
    view.Initialize(iniInfo, begInfo[0])
    view.UpdateEndData(cmd[0], endInfo[0])#bug
    view.show()
    sys.exit(app.exec_())
