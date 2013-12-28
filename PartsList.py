__author__ = 'Peeranut'

from PySide.QtGui import *
from PySide.QtCore import *


class PartsList(QListView):
    def __init__(self, parent):
        super().__init__(parent)

        #Set separation between each parts
        self.setGridSize(QSize(108, 80))

        # Create parts model
        self.partsModel = LibraryModel(self)

        # Add parts
        self.partsModel.appendRow(self.__getPartItem("SWITCH"))
        self.partsModel.appendRow(self.__getPartItem("WEB_SWITCH"))
        self.partsModel.appendRow(self.__getPartItem("CLOCK"))
        self.partsModel.appendRow(self.__getPartItem("BULB"))
        self.partsModel.appendRow(self.__getPartItem("PHUE"))
        self.partsModel.appendRow(self.__getPartItem("SOUND"))
        self.partsModel.appendRow(self.__getPartItem("AND"))
        self.partsModel.appendRow(self.__getPartItem("OR"))
        self.partsModel.appendRow(self.__getPartItem("NOT"))
        self.partsModel.appendRow(self.__getPartItem("NAND"))
        self.partsModel.appendRow(self.__getPartItem("NOR"))
        self.partsModel.appendRow(self.__getPartItem("XOR"))
        self.partsModel.appendRow(self.__getPartItem("XNOR"))

        # Set model
        self.setModel(self.partsModel)

        # Show image and text
        self.setViewMode(self.IconMode)

        # Only dragging parts out are allowed
        self.setDragDropMode(self.DragOnly)

    def __getPartItem(self, name):
        part = QStandardItem()
        pixmap = QPixmap("image/" + name + ".png")
        part.setData(pixmap, Qt.DecorationRole)
        part.setText(name)
        part.setEditable(False)
        return part


class LibraryModel(QStandardItemModel):
    def __init__(self, parent=None):
        QStandardItemModel.__init__(self, parent)
        self.setColumnCount(1)

    def mimeTypes(self):
        return ['part/name']

    def mimeData(self, idxs):
        mimedata = QMimeData()
        for idx in idxs:
            if idx.isValid():
                txt = self.data(idx, Qt.DisplayRole)
                mimedata.setData('part/name', txt)
        return mimedata