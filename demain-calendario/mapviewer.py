#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore

class MapViewer(QtGui.QGraphicsView):
	def __init__(self, scene, parent, imagePath):
		super(MapViewer, self).__init__(scene, parent)
		self.setScene(scene)
		self.parent = parent
		self.setSceneRect(0,0, parent.width(), parent.height())
		self.pixmapScaled = QtGui.QPixmap(imagePath).scaled( self.parent.width(), self.parent.height())
		self.scene().addPixmap(self.pixmapScaled)
		self.show()
		
	def setBackgroundImage(self, imagePath):
		pixmap = QtGui.QPixmap(imagePath)
		pixmapScaled = pixmap.scaled( self.parent.width(), self.parent.height())
		self.scene.addPixmap(pixmapScaled)
		self.show()
		
	def drawCerca(self, cerca):
		poly = QtGui.QPolygonF()
		for p in cerca:
			poly.append(QtCore.QPointF(float(p["x"]),float(p["y"])))
		self.scene().addPolygon(poly,QtGui.QPen(QtCore.Qt.magenta,4))
		self.show()

	#def showEvent(self, event) :
		#self.fitInView(self.scene().sceneRect(),QtGui.KeepAspectRatio);
	
	#EVENTO RESIZE
	#def resizeEvent(self, evt=None):
		#print "resize"
		#self.scene().addPixmap(self.pixmapScaled.scaled( self.parent.width(), self.parent.height()))
		#self.show()
		##self.emit(SIGNAL("resize()"))
	
	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			print "Pressed"