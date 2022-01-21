from ..predefined_components import PredefinedComponent
from ...components import Circle, Text


class PMSM(PredefinedComponent):
    def __init__(self, position, doc=None):
        super().__init__()
        self._position = position
        self._circle = Circle(position, text=Text(['PMSM']), inputs=dict(left=3))

        if doc is not None:
            doc.append(self)

    def build(self, pic):
        self._circle.build(pic)
