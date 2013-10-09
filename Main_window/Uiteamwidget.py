#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#制作团队界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import qrc_resource
class TeamScrollWidget(QWidget):
	def __init__(self, parent = None):
		super(TeamScrollWidget, self).__init__(parent)

		self.text = None
		self.offset = 0

		pal = self.palette()
		pal.setColor(QPalette.WindowText, QColor(255, 255, 255))
		pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
		self.setPalette(pal)

		#字体
#		font = self.font()
#		font.set
#		self.setFont(font)
		#语系
		QTextCodec.setCodecForTr(QTextCodec.codecForName("system"))

	def setText(self, text):
		self.text = QString.fromUtf8(text)
		self.update()
		self.updateGeometry()

	def sizeHint(self):
		return self.fontMetrics().size(0, self.text)

	def showEvent(self, event):
		self.myTimerId = self.startTimer(50)
	#close 也会调用
	def hideEvent(self, event):
		self.killTimer(self.myTimerId)

	def timerEvent(self, event):
		if event.timerId() == self.myTimerId:
			self.offset += 1
			if self.offset >= self.fontMetrics().width(self.text)/6:
				self.offset = 0
			self.scroll(-1, 0)
		else:
			QWidget.timerEvent(self, event)

	def paintEvent(self, event):
		painter = QPainter(self)
		#scroll widget background
	  #  painter.fillRect(QRect(0,0,self.width(),self.height()),QBrush(Qt.black))
		textWidth = self.fontMetrics().width(self.text)
		x =  500 - self.offset

		while x < self.width():# self.width():
			painter.drawText(x, 0, textWidth, self.height(),
							 Qt.AlignLeft | Qt.AlignVCenter, self.text)
			x += textWidth

class TeamWidget(QWidget):
	def __init__(self, parent = None):
		super(TeamWidget, self).__init__(parent)

		self.title = "制作团队"
		self.titleLabel = QLabel(QString.fromUtf8(self.title))
		self.scrollWidget = TeamScrollWidget()
		self.returnButton = QPushButton()
		self.returnButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.returnButton.resize(140, 30)
		self.returnButton.setStyleSheet("*{border-image: url(:return0.png);border: 0;}"
										"*:hover{border-image: url(:return1.png);border: 0;}")

		self.text = \
			"																														   \n\
	   指	 孙  牟  俞  庄  武	    开	   逻   朴  刘     平   李  胡     网   池  陈     展   谈  王     界   李  宁  李	  \n\
             泽	     翔  程  倩	    发     辑   镜  帅     台   步  益     站   雨  浩     示   志         面   栋  雪		  \n\
	   导	 雷  瞳  宇  旭  聿	    组	   组   谭  祎     组   宇  铭     组   泽  贤     组   勋  康     组   林  妃  根	  \n"
		self.scrollWidget.setText(self.text)
		pal = self.palette()
		pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
		pal.setColor(QPalette.WindowText, QColor(255, 255, 255))
		self.setPalette(pal)
		self.setAutoFillBackground(True)

		hlayout1 = QHBoxLayout()
		hlayout1.addStretch()
		hlayout1.addWidget(self.titleLabel)
		hlayout1.addStretch()

		hlayout2 = QHBoxLayout()
		hlayout2.addStretch()
		hlayout2.addWidget(self.returnButton)
		hlayout2.addStretch()

		vlayout = QVBoxLayout()
		vlayout.addStretch(1)
		vlayout.addLayout(hlayout1)
		vlayout.addStretch(1)
		vlayout.addWidget(self.scrollWidget)
		vlayout.addStretch(2)
		vlayout.addLayout(hlayout2)
		self.setLayout(vlayout)
		self.resize(1000, 564)
if __name__ == "__main__":
	import sys
   # text = \
   # "																				 \n\
   #	指	 孙  牟		开	 逻  朴  刘			展  谈  王			  \n\
   #		   泽			发	 辑  镜  帅			示  志				  \n\
   #	导	 雷  瞳		组	 组  谭  祎			组  勋  康			  \n"
	app = QApplication(sys.argv)
	widget = TeamWidget()
   # widget.setText(text)
	widget.show()
   # print text
	app.exec_()
