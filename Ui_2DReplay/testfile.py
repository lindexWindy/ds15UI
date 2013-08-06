# -*- coding: UTF-8 -*-

from Ui_ReplayWidget import *
from testdata import *


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_2DReplayWidget(scene)
    view.setBackgroundBrush(QtGui.QColor(0, 0, 0))
    view.Initialize(iniInfo, begInfo0)
    view.UpdateEndData(cmd0, endInfo0)#bug(OK)
    view.UpdateBeginData(begInfo1)
    view.UpdateEndData(cmd1, endInfo1)
    view.GoToRound(1, 0)
    cursor = Ui_TargetCursor()
    scene.addItem(cursor)
    cursor.setPos(QtCore.QPointF(0, 0))
    
    #view.ShowMoveAnimation()#bug
    view.show()
    sys.exit(app.exec_())
