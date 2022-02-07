from ..predefined_components import PredefinedComponent
from control_block_diagram.components import Circle


class Add(PredefinedComponent):

    def __init__(self, position, radius: float = 0.15, inputs: dict = dict(left=1, bottom=1),
                 outputs: dict = dict(right=1), doc=None):
        super().__init__(position, doc)
        self._circle = Circle(position, radius, inputs=inputs, outputs=outputs)

        self.input = self._circle.input_dict
        self.output = self._circle.output_dict
        self.border = self._circle.border

    def build(self, pic):
        self._circle.build(pic)
