from pylatex import TikZDraw, TikZOptions
import numpy as np
from ..block import Block
from ...points import Point, Input, Output, Center
from ...text import Text


class Circle(Block):

    @property
    def size(self):
        return self._radius, self._radius

    def __init__(self, position: (Point, Center), radius: float = 1, text: Text = None, draw: str = 'black', fill: str = 'white',
                 space: float = 1.5, input_left: int = 1, input_top: int = 0, input_right: int = 0,
                 input_bottom: int = 0, output_left: int = 0, output_top: int = 0, output_right: int = 1,
                 output_bottom: int = 0, doc=None):
        super().__init__(Center.convert(position), fill, draw, text, (radius * 2, radius * 2), space, doc)
        self._radius = radius
        self._define_in_output(input_left, input_top, input_right, input_bottom, output_left, output_top, output_right,
                               output_bottom)

    def _define_in_output(self, input_left: int, input_top: int, input_right: int, input_bottom: int, output_left: int,
                          output_top: int, output_right: int, output_bottom: int):

        in_out_dict = {'left': ('west', -1),
                       'top': ('north', 1),
                       'right': ('east', 1),
                       'bottom': ('south', -1)}

        self._input_left = self._get_in_output(in_out_dict['left'], Input, input_left)
        self._input_top = self._get_in_output(in_out_dict['top'], Input, input_top)
        self._input_right = self._get_in_output(in_out_dict['right'], Input, input_right)
        self._input_bottom = self._get_in_output(in_out_dict['bottom'], Input, input_bottom)

        self._output_left = self._get_in_output(in_out_dict['left'], Output, output_left)
        self._output_top = self._get_in_output(in_out_dict['top'], Output, output_top)
        self._output_right = self._get_in_output(in_out_dict['right'], Output, output_right)
        self._output_bottom = self._get_in_output(in_out_dict['bottom'], Output, output_bottom)

    def _get_in_output(self, in_out_dict, in_out, count):
        direction, sign = in_out_dict
        if direction in ['west', 'east']:
            y_list = [(0.5 - (y + 1) / (count + 1)) * self._size_y for y in range(count)]
            x_list = [sign * np.cos(np.arcsin(y / self._radius)) * self._radius for y in y_list]
        elif direction in ['north', 'south']:
            x_list = [(0.5 - (x + 1) / (count + 1)) * self._size_y for x in range(count)]
            y_list = [sign * np.sin(np.arccos(x / self._radius)) * self._radius for x in x_list]
        return [in_out.convert(self._position.add(x, y, direction)) for x, y in zip(x_list, y_list)]

    def build(self, pic):
        circle = TikZDraw([self._position.tikz, 'circle'],
                          options=TikZOptions(radius=str(self._radius) + 'cm', draw=self._draw, fill=self._fill))
        pic.append(circle)
        super().build(pic)
