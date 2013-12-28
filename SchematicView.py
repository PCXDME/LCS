__author__ = 'Peeranut'

from Connector import *
from Part import *
import parts.SWITCH
import parts.WEB_SWITCH
import parts.CLOCK
import parts.BULB
import parts.PHUE
import parts.SOUND
import parts.AND_GATE
import parts.OR_GATE
import parts.NOT_GATE
import parts.NAND_GATE
import parts.NOR_GATE
import parts.XOR_GATE
import parts.XNOR_GATE


class SchematicView(QGraphicsView):
    def __init__(self, parent):
        self.scene = SchematicScene()
        super().__init__(self.scene, parent)
        self.setSceneRect(0, 0, 1, 1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('part/name'):
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('part/name'):
            event.accept()

    # When user drop the part into the schematic view
    def dropEvent(self, event):
        if event.mimeData().hasFormat('part/name'):
            name = str(event.mimeData().data('part/name'))

            part_list = {"SWITCH": parts.SWITCH.SWITCH,
                         "WEB_SWITCH": parts.WEB_SWITCH.WEB_SWITCH,
                         "CLOCK": parts.CLOCK.CLOCK,
                         "BULB": parts.BULB.BULB,
                         "PHUE": parts.PHUE.PHUE,
                         "SOUND": parts.SOUND.SOUND,
                         "AND": parts.AND_GATE.AND_GATE,
                         "OR": parts.OR_GATE.OR_GATE,
                         "NOT": parts.NOT_GATE.NOT_GATE,
                         "NAND": parts.NAND_GATE.NAND_GATE,
                         "NOR": parts.NOR_GATE.NOR_GATE,
                         "XOR": parts.XOR_GATE.XOR_GATE,
                         "XNOR": parts.XNOR_GATE.XNOR_GATE}

            p = part_list[name]()
            p.setPos(self.mapToScene(event.pos()))
            self.scene.addItem(p)


class SchematicScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # No current connector at initial
        self.currentConnector = None

    def mouseMoveEvent(self, mouseEvent):
        # When drag the wire
        if self.currentConnector:
            pos = mouseEvent.scenePos()
            if self.currentConnector.start is None:
                self.currentConnector.startpos = pos
            elif self.currentConnector.end is None:
                self.currentConnector.endpos = pos
            self.currentConnector.update()
        super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        # When release the wire
        if self.currentConnector:
            pos = mouseEvent.scenePos()
            items = self.items(pos)
            for item in items:
                if type(item) is ConnectionPort:
                    # Check if connection connects form input to output
                    if self.currentConnector.start is None and item.name >= 'p':
                        if self.currentConnector.end.part != item.part:
                            self.currentConnector.start = item
                            item.connection.append(self.currentConnector)
                            self.currentConnector.start.part.evaluate()
                    # Check if connection connects form output to input and input can have only one connection
                    elif self.currentConnector.end is None and item.name < 'p' and len(item.connection) == 0:
                        if self.currentConnector.start.part != item.part:
                            self.currentConnector.end = item
                            item.connection.append(self.currentConnector)
                            self.currentConnector.start.part.evaluate()
                    self.currentConnector.update()
            if self.currentConnector.start is None or self.currentConnector.end is None:
                self.currentConnector.delete()

            self.currentConnector = None
        super().mouseReleaseEvent(mouseEvent)

    # Call when clicked on a port
    def startConnection(self, port):
        # Create a connector
        if port.name >= 'p':
            self.currentConnector = Connector(port, None)
        elif len(port.connection) == 0:
            self.currentConnector = Connector(None, port)
        self.addItem(self.currentConnector)