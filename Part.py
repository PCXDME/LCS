__author__ = 'Peeranut'

import sys

from PySide import QtGui, QtCore
from PySide.QtGui import *
from PySide.QtCore import *


class Part(QGraphicsPixmapItem):
    def __init__(self, name):
        super().__init__()
        self.name = name

        # Make part selectable, movable and focusable
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable | self.ItemIsFocusable)

        # Set cursor to hand cursor while mouse is over
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Set Image
        self.pixmap = QPixmap("image/" + name + ".png")
        self.pixmap_on = QPixmap("image/" + name + "_ON.png")
        self.setPixmap(self.pixmap)

        # Create Inputs and Outputs port of the part
        self.inputs = {}
        self.outputs = {}

    def keyPressEvent(self, event):
        # Press delete key to delete part
        if (event.matches(QKeySequence.Delete)):
            self.delete()

    def contextMenuEvent(self, event):
        # Right click context
        menu = QMenu()
        info = menu.addAction('Info')
        info.triggered.connect(self.showInfo)
        delete = menu.addAction('Delete')
        delete.triggered.connect(self.delete)
        menu.exec_(event.screenPos())

    def showInfo(self):
        pass

    def delete(self):
        # Delete all connection connected to the part
        for input in self.inputs:
            while len(self.inputs[input].connection) > 0:
                self.inputs[input].connection[0].delete()
        for output in self.outputs:
            while len(self.outputs[output].connection) > 0:
                self.outputs[output].connection[0].delete()
            # Delete the part
        self.scene().removeItem(self)

    def getInputValue(self, name):
        state = False
        if len(self.inputs[name].connection) == 1:
            state = self.inputs[name].connection[0].value
        return state

    def check(self, a, b, output):
        pass

    def evaluate(self):
        inVal = []
        for i in self.inputs:
            inVal.append(self.getInputValue(i))
        for o in self.outputs:
            result = self.check(*(inVal + [o]))
            for c in self.outputs[o].connection:
                c.set(result)
            if result:
                self.setPixmap(self.pixmap_on)
            else:
                self.setPixmap(self.pixmap)


class InfoDialog(QDialog):
    def __init__(self, part):
        super().__init__()

        self.part = part

        # Set window title
        self.setWindowTitle("Info")

        # Create Layout
        infoDialog = QVBoxLayout(self)

        # Create Labels
        self.name = QLabel("Name: " + part.name)

        # Get evaluate table
        self.table = self.__getTable()

        # Create OK Button
        self.button = QPushButton("OK", self)
        self.button.clicked.connect(self.OK)

        # Add Objects to Layout
        infoDialog.addWidget(self.name)
        inVal = []
        for i in self.part.inputs:
            infoDialog.addWidget(QLabel("'" + i + "'->: " + str(part.getInputValue(i))))
            inVal.append(part.getInputValue(i))
        for o in self.part.outputs:
            infoDialog.addWidget(QLabel("->'" + o + "': " + str(part.check(*(inVal + [o])))))
        infoDialog.addWidget(self.table)
        infoDialog.addWidget(self.button)

    def OK(self):
        self.close()

    def __getTable(self):
        table = QtGui.QTableWidget()
        table.setRowCount(2 ** len(self.part.inputs))
        table.setColumnCount(len(self.part.inputs) + len(self.part.outputs))

        # Set column width
        for i in range(len(self.part.inputs) + len(self.part.outputs)):
            table.setColumnWidth(i, 50)

        header = []
        for i in self.part.inputs:
            header.append("Input\n'" + i + "'")
        for o in self.part.outputs:
            header.append("Output\n'" + o + "'")

        table.setHorizontalHeaderLabels(header)

        table.setVerticalHeaderLabels(["" for i in range(2 ** len(self.part.inputs))])

        # Make not editable and not selectable
        table.setDisabled(True)

        for i in range(0, 2 ** len(self.part.inputs)):
            inVal = []
            for j in range(len(self.part.inputs)):
                state = True if i >> (len(self.part.inputs) - j - 1) & 1 else False
                table.setItem(i, j, QtGui.QTableWidgetItem(str(state)))
                inVal.append(state)

            for j in range(len(self.part.outputs)):
                table.setItem(i, len(self.part.inputs) + j,
                              QtGui.QTableWidgetItem(str(self.part.check(*(inVal + [j])))))

        return table


class ConnectionPort(QGraphicsEllipseItem):
    def __init__(self, name, part):
        self.part = part
        # Init port with size of 12x12 at center
        super().__init__(QRectF(-6, -6, 12, 12), part)

        # Normal Arrow Cursor when mouse is over
        self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        # Set Appearance:
        self.setBrush(QBrush(Qt.white))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 1))

        # Set name
        self.name = name

        self.connection = []
        self.setFlag(self.ItemSendsScenePositionChanges, True)

    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged:
            for c in self.connection:
                c.update()
            return value
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        self.scene().startConnection(self)