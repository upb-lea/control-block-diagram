from ..control_diagram import ControllerDiagram


class Component:

    def __init__(self, doc: ControllerDiagram = None):
        if isinstance(doc, ControllerDiagram):
            doc.append(self)

    def build(self, pic):
        pass
