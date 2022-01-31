from control_block_diagram.predefined_components.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Circle, Text, Center


class ElectricMotor(PredefinedComponent):
    def __init__(self, position, text, size=1.5, input: str = 'left', input_number: int = 1, output: str = 'right',
                 output_number: int = 2, doc=None,):
        super().__init__()
        self._position = position
        self._circle = Circle(position, radius=size / 2, text=Text(text), inputs={input: input_number},
                              outputs={output: output_number, output + '_space': 0.3}, )

        box_pos = (self._circle.output[0] + self._circle.output[1]) / 2
        if output == 'right':
            self._box = Box(box_pos, (size * 2 / 3, (self._circle.output[0] - self._circle.output[1]).y))
            self._circle_2 = Circle(box_pos.add_x(size/3), radius=(self._circle.output[0] - self._circle.output[1]).y)
        elif output == 'top':
            self._box = Box(Center.convert(box_pos, horizontal=True, vertical=False),
                            ((self._circle.output[0] - self._circle.output[1]).x, size * 2 / 3))
            self._circle_2 = Circle(box_pos.add_y(size/3), radius=(self._circle.output[0] - self._circle.output[1]).x)
        elif output == 'bottom':
            self._box = Box(Center.convert(box_pos, horizontal=True, vertical=False),
                            ((self._circle.output[0] - self._circle.output[1]).x, size * 2 / 3))
            self._circle_2 = Circle(box_pos.sub_y(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).x)
        elif output == 'left':
            self._box = Box(box_pos, (size * 2 / 3, (self._circle.output[0] - self._circle.output[1]).y))
            self._circle_2 = Circle(box_pos.sub_x(size/3), radius=(self._circle.output[0] - self._circle.output[1]).y)

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
        self._box.build(pic)
        self._circle_2.build(pic)
        self._circle.build(pic)
