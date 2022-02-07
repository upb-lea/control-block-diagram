from control_block_diagram.predefined_components.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Circle, Text, Center, Point, Path
from pylatex import TikZDraw, TikZUserPath, TikZOptions


class ElectricMotor(PredefinedComponent):
    def __init__(self, position, text, size=1.5, input: str = 'left', input_number: int = 1, output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.3, doc=None):
        super().__init__(position, doc)
        self._size = size
        self._circle = Circle(position, radius=size / 2, text=Text(text),
                              inputs={input: input_number, input + '_space': input_space},
                              outputs={orientation: 2, orientation + '_space': size * 0.2})

        box_pos = (self._circle.output[0] + self._circle.output[1]) / 2
        if orientation == 'right':
            self._box = Box(box_pos, (size * 2 / 3, (self._circle.output[0] - self._circle.output[1]).y))
            self._circle_2 = Circle(box_pos.add_x(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
        elif orientation == 'top':
            self._box = Box(Center.convert(box_pos, horizontal=True, vertical=False),
                            ((self._circle.output[0] - self._circle.output[1]).x, size * 2 / 3))
            self._circle_2 = Circle(box_pos.add_y(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
        elif orientation == 'bottom':
            self._box = Box(Center.convert(box_pos, horizontal=True, vertical=False),
                            ((self._circle.output[0] - self._circle.output[1]).x, size * 2 / 3))
            self._circle_2 = Circle(box_pos.sub_y(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
        elif orientation == 'left':
            self._box = Box(box_pos, (size * 2 / 3, (self._circle.output[0] - self._circle.output[1]).y))
            self._circle_2 = Circle(box_pos.sub_x(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})

        self._path = Path([self._box.bottom_left.sub(self._size * 0.3, self._size * 0.05),
                           ((self._box.bottom_left + self._box.bottom_right) / 2).sub_y(self._size * 0.15),
                           self._box.bottom_right.add(self._size * 0.3, -self._size * 0.05)],
                          angles=[{'in': 180, 'out': -55}, {'in': -135, 'out': 0}],
                          text=r'$T, \omega$', text_align='bottom', distance_y=size * 0.2)

        self.input = self._circle.input_dict
        self.output = self._circle_2.output_dict

    def build(self, pic):
        self._box.build(pic)
        self._circle_2.build(pic)
        self._circle.build(pic)
        self._path.build(pic)
