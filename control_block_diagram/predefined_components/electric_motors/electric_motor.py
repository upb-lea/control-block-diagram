from ..predefined_components import PredefinedComponent
from ...components import Circle, Text


class ElectricMotor(PredefinedComponent):
    def __init__(self, position, text, size=1.5, input: str = 'left', input_number: int = 1, output: str = None,
                 output_number: int = 0, doc=None,):
        super().__init__()
        self._position = position
        self._circle = Circle(position, radius=size / 2, text=Text([text]), inputs={input: input_number},
                              outputs={output: output_number})

        self.input_left = self._circle.input_left
        self.input_top = self._circle.input_top
        self.input_right = self._circle.input_right
        self.input_bottom = self._circle.input_bottom

        self.output_left = self._circle.output_left
        self.output_top = self._circle.output_top
        self.output_right = self._circle.output_right
        self.output_bottom = self._circle.output_bottom

        if doc is not None:
            doc.append(self)

    def build(self, pic):
        self._circle.build(pic)
