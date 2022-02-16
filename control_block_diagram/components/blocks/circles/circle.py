from pylatex import TikZDraw, TikZOptions
import numpy as np
from ..block import Block
from ...points import Point, Input, Output, Center
from ...text import Text


class Circle(Block):

    @property
    def size(self):
        return self._radius, self._radius

    def __init__(self, position: (Point, Center), radius: float = 1, text: Text = None, draw: str = 'black',
                 fill: str = 'white', space: float = 1.5, inputs: dict = dict(left=1),
                 outputs: dict = dict(right=1), doc=None):
        super().__init__(Center.convert(position), fill, draw, text, (radius * 2, radius * 2), space, doc)
        self._radius = radius

        input_dict = {'left': ('west', -1, inputs.get('left', 0), Input, inputs.get('left_space', None),
                               inputs.get('left_text', ())),
                      'top': ('north', 1, inputs.get('top', 0), Input, inputs.get('top_space', None),
                              inputs.get('top_text', ())),
                      'right': ('east', 1, inputs.get('right', 0), Input, inputs.get('right_space', None),
                                inputs.get('right_text', ())),
                      'bottom': ('south', -1, inputs.get('bottom', 0), Input, inputs.get('bottom_space', None),
                                 inputs.get('bottom_text', ()))}

        output_dict = {'left': ('west', -1, outputs.get('left', 0), Output, outputs.get('left_space', None),
                                outputs.get('left_text', ())),
                       'top': ('north', 1, outputs.get('top', 0), Output, outputs.get('top_space', None),
                               outputs.get('top_text', ())),
                       'right': ('east', 1, outputs.get('right', 0), Output, outputs.get('right_space', None),
                                 outputs.get('right_text', ())),
                       'bottom': ('south', -1, outputs.get('bottom', 0), Output, outputs.get('bottom_space', None),
                                  outputs.get('bottom_text', ()))}

        self.set_in_output(input_dict, output_dict, self._get_in_output)

    def _get_in_output(self, in_out_dict):
        direction, sign, count, in_out, space, _ = in_out_dict
        y_list = Block.get_in_out_list(self._radius * 2, space, count)
        '''
        if count > 1:
            space = (self._radius * 2 - 2 * space) / (count - 1)
            y_list = [(0.5 - (i / (count - 1))) * space for i in range(count)]
        elif count == 1:
            y_list = [self._radius]
        else:
            y_list = []
        '''
        if direction in ['west', 'east']:
            x_list = [sign * np.cos(np.arcsin(y / self._radius)) * self._radius for y in y_list]
        elif direction in ['north', 'south']:
            x_list = y_list
            y_list = [sign * np.sin(np.arccos(x / self._radius)) * self._radius for x in x_list]
        return [in_out.convert(self._position.add(x, y, direction)) for x, y in zip(x_list, y_list)]

    def build(self, pic):
        circle = TikZDraw([self._position.tikz, 'circle'],
                          options=TikZOptions(radius=str(self._radius) + 'cm', **self._tikz_options))
        pic.append(circle)
        super().build(pic)
