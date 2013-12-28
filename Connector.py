__author__ = 'Peeranut'

from PySide import QtGui, QtCore
from PySide.QtGui import *
from PySide.QtCore import *


class Connector(QGraphicsLineItem):
    def __init__(self, start, end):
        super().__init__()
        self.value = None

        # Set an appearance
        self.setPen(QtGui.QPen(QtCore.Qt.black, 5))

        # Make connector selectable and focusable
        self.setFlags(self.ItemIsSelectable | self.ItemIsFocusable)

        self.start = start
        self.end = end

        if self.start is not None:
            self.startpos = start.scenePos()
            self.endpos = start.scenePos()
            self.start.connection.append(self)
        if self.end is not None:
            self.startpos = end.scenePos()
            self.endpos = end.scenePos()
            self.end.connection.append(self)
        self.update()
        # Bring to back
        self.setZValue(-100)

        self.value = False

    def update(self):
        if self.start:
            self.startpos = self.start.scenePos()
        if self.end:
            self.endpos = self.end.scenePos()
        self.setLine(QLineF(self.startpos, self.endpos))

    # Right click to delete connection
    def contextMenuEvent(self, event):
        self.delete()

    def keyPressEvent(self, event):
        # Delete when press delete button
        if event.matches(QKeySequence.Delete):
            self.delete()

    def delete(self):
        self.set(False)
        if self.start:
            self.start.connection.remove(self)
        if self.end:
            self.end.connection.remove(self)
        self.scene().removeItem(self)

    def set(self, value):
        if self.value == value:
            return
        self.value = value
        if self.value:
            self.setPen(QtGui.QPen(QtCore.Qt.red, 5))
        else:
            self.setPen(QtGui.QPen(QtCore.Qt.black, 5))

        if self.end:
            self.end.part.evaluate()
