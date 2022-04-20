from pylatex import TikZDraw, TikZOptions
import numpy as np
from ..block import Block
from ...points import Point, Input, Output, Center
from ...text import Text


class Circle(Block):
    """Circle with inputs, outputs and text"""

    @property
    def size(self):
        """Returns the size of a circle"""
        return self._radius, self._radius

    def __init__(self, position: (Point, Center), radius: float = 1, text: (Text, str) = None,
                 inputs: dict = dict(left=1), outputs: dict = dict(right=1), text_configuration: dict = dict(),
                 level: int = 0, *args, **kwargs):
        """
        Initializes a circle and adds it to the active document

             :param position:   center of the circle
             :param radius:     radius of the circle
             :param text:       text inside the box
             :param inputs:     dictonary with the configuration of the inputs of a circle, possible keys:
                                left, right, top, bottom:   number of inputs on each side
                                "side" + _space:            distance of inputs on this side
                                "side" + _text:             list with the texts at the inputs of this side
                                "side" + _text_space:       distance of the text to the inputs of this side
             :param outputs:    dictonary with the configuration of the inputs of a circle, same possible keys as for inputs
             :param text_configuration: dictionary of arguments passed to the text
             :param level:      level of the component
        """

        super().__init__(Center.convert(position), text, (radius * 2, radius * 2), text_configuration, level, *args,
                         **kwargs)
        self._radius = radius   # Set the radius

        # Define inputs and outputs of the circle
        input_dict = {'left': ('west', -1, inputs.get('left', 0), Input, inputs.get('left_space', None),
                               inputs.get('left_text_space', 0.2), inputs.get('left_text', ())),
                      'top': ('north', 1, inputs.get('top', 0), Input, inputs.get('top_space', None),
                              inputs.get('top_text_space', 0.2), inputs.get('top_text', ())),
                      'right': ('east', 1, inputs.get('right', 0), Input, inputs.get('right_space', None),
                                inputs.get('right_text_space', 0.2), inputs.get('right_text', ())),
                      'bottom': ('south', -1, inputs.get('bottom', 0), Input, inputs.get('bottom_space', None),
                                 inputs.get('bottom_text_space', 0.2), inputs.get('bottom_text', ()))}

        output_dict = {'left': ('west', -1, outputs.get('left', 0), Output, outputs.get('left_space', None),
                                outputs.get('left_text_space', 0.2), outputs.get('left_text', ())),
                       'top': ('north', 1, outputs.get('top', 0), Output, outputs.get('top_space', None),
                               outputs.get('top_text_space', 0.2), outputs.get('top_text', ())),
                       'right': ('east', 1, outputs.get('right', 0), Output, outputs.get('right_space', None),
                                 outputs.get('right_text_space', 0.2), outputs.get('right_text', ())),
                       'bottom': ('south', -1, outputs.get('bottom', 0), Output, outputs.get('bottom_space', None),
                                  outputs.get('bottom_text_space', 0.2), outputs.get('bottom_text', ()))}

        self.set_in_output(input_dict, output_dict, self._get_in_output, level)

    def _get_in_output(self, in_out_dict):
        """Function to calculate the positions of the inputs and outputs"""
        direction, sign, count, in_out, space, _, _ = in_out_dict
        y_list = Block.get_in_out_list(self._radius * 2, space, count)

        if direction in ['west', 'east']:
            x_list = [sign * np.cos(np.arcsin(y / self._radius)) * self._radius for y in y_list]
        elif direction in ['north', 'south']:
            x_list = y_list
            y_list = [sign * np.sin(np.arccos(x / self._radius)) * self._radius for x in x_list]
        return [in_out.convert(self._position.add(x, y, direction)) for x, y in zip(x_list, y_list)]

    def build(self, pic):
        """Funtion to add the Latex code to the Latex document"""
        circle = TikZDraw([self._position.tikz, 'circle'],
                          options=TikZOptions(radius=str(self._radius) + 'cm', *self._style_args, **self._tikz_options))
        pic.append(circle)
        super().build(pic)
