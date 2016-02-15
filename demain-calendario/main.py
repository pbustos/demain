#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from PySide import QtGui, QtCore
print QtGui.__file__
from pprint import pprint
import pyqtgraph as pg
import numpy as np
from mapviewer import MapViewer

from subprocess import call

call("pyside-uic demain.ui > ui_demain.py", shell=True)
from ui_demain import Ui_Demain

mapaColores={}
mapaColores["otras intervenciones"] = QtGui.QColor(QtCore.Qt.red)
mapaColores["flusching-efecto macho"] = QtGui.QColor(QtCore.Qt.darkRed)
mapaColores["vacuna clamidia"] = QtGui.QColor(QtCore.Qt.green)
mapaColores["desparasitación con closantel"] = QtGui.QColor(QtCore.Qt.darkGreen)
mapaColores["Cubrición"] = QtGui.QColor(QtCore.Qt.blue)
mapaColores["CERCA-1"] = QtGui.QColor(QtCore.Qt.darkYellow)
mapaColores["CERCA-2"] = QtGui.QColor(QtCore.Qt.darkYellow)
mapaColores["CERCA-3"] = QtGui.QColor(QtCore.Qt.darkYellow)
mapaColores["CERCA-4"] = QtGui.QColor(QtCore.Qt.darkYellow)
mapaColores["CERCA-5"] = QtGui.QColor(QtCore.Qt.darkYellow)
mapaColores["CERCA-6"] = QtGui.QColor(QtCore.Qt.darkYellow)
mapaColores["Ecógrafo"] = QtGui.QColor(QtCore.Qt.darkCyan)
mapaColores["Mantener preñadas en esta cerca"] = QtGui.QColor(QtCore.Qt.magenta)
mapaColores["Pasar no preñadas a CERCA-1"] = QtGui.QColor(QtCore.Qt.darkMagenta)
mapaColores["Alimentación suplementaria"] = QtGui.QColor(QtCore.Qt.darkMagenta)
mapaColores["Paridera y lactancia"] = QtGui.QColor(QtCore.Qt.darkMagenta)

meses = ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre")
messages = (u"comenzar flusching-efecto macho",
		   u"suministrar vacuna clamidia",
		   u"desparasitación con closantel",
		   u"Inicio cubrición",
		   u"Mover lote 4 a CERCA-1",
		   u"Mover lote 2 a CERCA-2",
		   u"Pasar ecógrafo",
		   u"Mantener preñadas en esta cerca",
		   u"Pasar preñadas a CERCA-1")

  
class MainWindow(QtGui.QWidget, Ui_Demain):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.show()
		
		self.confJSON = self.readConfigurationJSON("config.json")
		self.calendarJSON = self.readConfigurationJSON("calendar.json", imprimir = False)
		
		#Property map
		self.scene = QtGui.QGraphicsScene(self)
		self.mapViewer = MapViewer(self.scene, self.scrollArea, "img/finca-pia.jpg")
		for cerca in self.confJSON["cercas"]:
			self.mapViewer.drawCerca( cerca["polilinea"] )
		
		#List of messages
		self.createMessages( self.messagesView)
		
		#self.scene = QtGui.QGraphicsScene(self)
		self.createCalendar( self.calendarJSON, self.calendarView)
	
		self.show()
	
		
	def readConfigurationJSON(self, fileName, imprimir = False):
		with open(fileName, 'r') as fileJson:
			data = json.load(fileJson)
                if imprimir == True:
                    pprint(data)
		return data
  
  
	def createCalendar(self, calJSON, calView):
		calView.setRowCount(10);
		calView.setColumnCount(12*4*2);
		#calView.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		calView.horizontalHeader().hide()
		calView.verticalHeader().hide()
		calView.setWordWrap(True)
		calView.setTextElideMode(QtCore.Qt.ElideNone)
		calView.setShowGrid(False)

		#Months span
		NROW = 1
		for i,c in zip(range(0,96,4), range(24)):
			calView.setSpan(NROW, i, NROW, 4)
			item = QtGui.QTableWidgetItem(meses[c%12])
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			brush = QtGui.QBrush(QtGui.QColor(128, 128, 128))
			brush.setStyle(QtCore.Qt.SolidPattern)
			item.setBackground(brush)
			font = QtGui.QFont()
			font.setFamily(u"DejaVu Sans")
			font.setPointSize(14)
			font.setBold(True)
			item.setFont(font)
			calView.setItem(NROW,i, item)
			
		#Weeks naming
		NROW = 2
		for col in range(calView.columnCount()):
			item = QtGui.QTableWidgetItem("semana " + str(col))
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
			brush.setStyle(QtCore.Qt.SolidPattern)
			item.setBackground(brush)
			calView.setItem(NROW,col, item)
			
		#Content      
		NROW = 3
		weeks = calJSON["weeks"]
		for week, actions in weeks.iteritems():
			column = int(week)-1
			row =  NROW
			nameAnt = ""
			for action in actions:
				item = QtGui.QTableWidgetItem(action["name"])
				item.setTextAlignment(QtCore.Qt.AlignCenter)
				#print action["name"]
				brush = QtGui.QBrush(mapaColores[action["name"].encode("utf_8")])
				brush.setStyle(QtCore.Qt.SolidPattern)
				item.setBackground(brush)
				font = QtGui.QFont()
				font.setFamily(u"DejaVu Sans")
				font.setPointSize(12)
				item.setFont(font)
				calView.setItem(row, column, item);
				row = row + 1
		
		
		#Merge cols with the same name
		NROW = 3
		for row in range(NROW, calView.rowCount()):
			textAnt = ""
			for col in range(calView.columnCount()):
				item = calView.item(row,col)
				if item is not None:
					#print item.text(), textAnt, "col", col, range(col,-1,-1)
					for c in range(col, -1, -1):
					#  print calView.item(NROW,c) is None, calView.item(NROW,c).text() != textAnt
						if (calView.item(row,c) is None) or (calView.item(row,c).text() != textAnt):
							break
							
					#[c for c in range(col, 0,-1) if calView.item(NROW,c) is not None and calView.item(NROW,c).text() == textAnt]
					#print c, col
					if c < col and c>0:
						calView.setSpan(row,c+1,1,calView.columnSpan(row,c+1)+1)
					if c < col and c==0:  #ÑAPA
						calView.setSpan(row,c,1,calView.columnSpan(row,c)+1)
					textAnt = item.text()
			
		calView.resizeRowsToContents()

	def createMessages(self, messagesView):
		messagesView.setRowCount(len(messages));
		messagesView.setColumnCount(2);
		#messagesView.horizontalHeader().hide()
		messagesView.verticalHeader().hide()
		messagesView.setWordWrap(True)
		messagesView.setTextElideMode(QtCore.Qt.ElideNone)
		font = QtGui.QFont()
		font.setFamily(u"DejaVu Sans")
		font.setPointSize(14)
		font.setBold(True)
		messagesView.horizontalHeader().setFont(font)
		messagesView.setHorizontalHeaderLabels(("Mensajes", "Enviar"))
		messagesView.setColumnWidth(0, messagesView.width()*0.85)
		messagesView.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		messagesView.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
		
		for m,row in zip(messages, range(len(messages))):
			item = QtGui.QTableWidgetItem(m)
			item.setTextAlignment(QtCore.Qt.AlignLeft)
			brush = QtGui.QBrush(QtCore.Qt.darkGray)
			brush.setStyle(QtCore.Qt.SolidPattern)
			item.setBackground(brush)
			font = QtGui.QFont()
			font.setFamily(u"DejaVu Sans")
			font.setPointSize(12)
			item.setFont(font)
			messagesView.setItem(row, 0, item)
			
			# send Button
			btn = QtGui.QPushButton(messagesView)
			btn.clicked.connect(self.sendMessage)
			btn.setIcon(QtGui.QIcon("rightArrow.png"))
			btn.setIconSize(QtCore.QSize(btn.width()*0.7,btn.height()*0.7))
			messagesView.setCellWidget(row, 1, btn)
			
			
		#messagesView.resizeColumnsToContents()
		messagesView.horizontalHeader().setStretchLastSection(True)
		
	def sendMessage(self):
		clickme = QtGui.qApp.focusWidget()
		index = self.messagesView.indexAt(clickme.pos())
		if index.isValid():
			print messages[index.row()]
			clickme.setIcon(QtGui.QIcon())
			clickme.setText("OK")
		
	#wheel event to scroll the calendar
	def wheelEvent(self,event):
		if QtGui.qApp.focusWidget() == self.calendarView:
			if event.delta()/120 > 0:
				self.calendarView.horizontalScrollBar().triggerAction(QtGui.QAbstractSlider.SliderSingleStepAdd)
			if event.delta()/120 < 0:
				self.calendarView.horizontalScrollBar().triggerAction(QtGui.QAbstractSlider.SliderSingleStepSub)
				
      
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	frame = MainWindow()
	frame.show()    
	app.exec_()