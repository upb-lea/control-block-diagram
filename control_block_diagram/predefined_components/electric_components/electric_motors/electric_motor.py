from control_block_diagram.predefined_components.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Circle, Path
from pylatex import TikZDraw, TikZUserPath, TikZOptions


class ElectricMotor(PredefinedComponent):
    def __init__(self, position, text, size=1.5, input: str = 'left', input_number: int = 1, output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.3, additional_inputs=dict()):
        super().__init__(position)
        self._size = size
        additional_inputs[input] = input_number
        additional_inputs[input + '_space'] = input_space
        self._circle = Circle(position, radius=size / 2, text=text,
                              inputs=additional_inputs,
                              outputs={orientation: 2, orientation + '_space': size * 0.2})

        box_pos = (self._circle.output[0] + self._circle.output[1]) / 2
        box_size = 2 / 3 * size
        if orientation == 'right':
            self._box = Box([self._circle.output_right[0], self._circle.output_right[1].add_x(box_size)])
            self._circle_2 = Circle(box_pos.add_x(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
            self._path = Path([self._box.top_right.add(self._size * 0.05, self._size * 0.1),
                               ((self._box.top_right + self._box.bottom_right) / 2).add_x(self._size * 0.15),
                               self._box.bottom_right.add(self._size * 0.05, -self._size * 0.1)],
                              angles=[{'in': 90, 'out': 315}, {'in': 45, 'out': -90}],
                              text=r'$T, \omega_{\mathrm{me}}$', text_align='right', distance_x=size * 0.25)

        elif orientation == 'top':
            self._box = Box([self._circle.output_top[0].add_y(box_size), self._circle.output_top[1]])
            self._circle_2 = Circle(box_pos.add_y(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
            self._path = Path([self._box.top_left.add(-self._size * 0.1, self._size * 0.05),
                               ((self._box.top_left + self._box.top_right) / 2).add_y(self._size * 0.15),
                               self._box.top_right.add(self._size * 0.1, self._size * 0.05)],
                              angles=[{'in': 180, 'out': 55}, {'in': 135, 'out': 0}],
                              text=r'$T, \omega_{\mathrm{me}}$', text_align='top', distance_x=size * 0.2)

        elif orientation == 'bottom':
            self._box = Box([self._circle.output_bottom[0], self._circle.output_bottom[1].sub_y(box_size)])
            self._circle_2 = Circle(box_pos.sub_y(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
            self._path = Path([self._box.bottom_left.sub(self._size * 0.1, self._size * 0.05),
                               ((self._box.bottom_left + self._box.bottom_right) / 2).sub_y(self._size * 0.15),
                               self._box.bottom_right.add(self._size * 0.1, -self._size * 0.05)],
                              angles=[{'in': 180, 'out': -55}, {'in': -135, 'out': 0}],
                              text=r'$T, \omega_{\mathrm{me}}$', text_align='bottom', distance_y=size * 0.2)

        elif orientation == 'left':
            self._box = Box([self._circle.output_left[0].sub_x(box_size), self._circle.output_left[1]])
            self._circle_2 = Circle(box_pos.sub_x(size / 3), radius=(self._circle.output[0] - self._circle.output[1]).abs * 0.9,
                                    outputs={output: 1})
            self._path = Path([self._box.top_left.add(-self._size * 0.05, self._size * 0.1),
                               ((self._box.top_left + self._box.bottom_left) / 2).sub_x(self._size * 0.15),
                               self._box.bottom_left.sub(self._size * 0.05, self._size * 0.1)],
                              angles=[{'in': 90, 'out': 215}, {'in': 135, 'out': -90}],
                              text=r'$T, \omega_{\mathrm{me}}$', text_align='left', distance_x=size * 0.25)

        self.input = self._circle.input_dict
        self.output = self._circle_2.output_dict
