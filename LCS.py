__author__ = 'Peeranut'

from PartsList import *
from SchematicView import *


class LCS(QWidget):
    def __init__(self):
        super().__init__()
        # Set Window Title
        self.setWindowTitle("Logic Circuit Simulator")

        # Main Widget layout
        self.mainlLayout = QtGui.QHBoxLayout(self)

        # Left Parts Panel
        self.partsPanel = PartsList(self)
        # Schematic View
        self.schematicView = SchematicView(self)

        # Add Parts Panel and Schematic Scene to Main Widget
        self.mainlLayout.addWidget(self.partsPanel, 1)
        self.mainlLayout.addWidget(self.schematicView, 9)

# Delete items with thread
def deleteThread():
    toBeDelete = []
    for i in lcs.schematicView.items():
        if 'thread' in vars(i):
            toBeDelete.append(i)
    while len(toBeDelete) != 0:
        toBeDelete[0].delete()
        toBeDelete.remove(toBeDelete[0])


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    lcs = LCS()
    lcs.showMaximized()
    app.aboutToQuit.connect(deleteThread)
    app.exec_()