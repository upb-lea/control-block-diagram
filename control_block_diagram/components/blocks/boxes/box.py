from pylatex import TikZDraw, TikZOptions
from ..block import Block
from ...points import Point, Input, Output


class Box(Block):
    """
        Rectangular box with text and inputs and outputs
    """
    def __init__(self, position: (Point, list, tuple), size: tuple = (2.5, 1.5), text: str = None,
                 inputs: dict = dict(left=1), outputs: dict = dict(right=1), text_configuration: dict = dict(),
                 level: int = 0, *args, **kwargs):
        """
        Initializes a box and adds it to the active document

            :param position:   center of the box or top left and bottom right point of the box
            :param size:       size of the box in x and y direction
            :param text:       text inside the box
            :param inputs:     dictonary with the configuration of the inputs of a box, possible keys:
                                left, right, top, bottom:   number of inputs on each side
                                "side" + _space:            distance of inputs on this side
                                "side" + _text:             list with the texts at the inputs of this side
                                "side" + _text_space:       distance of the text to the inputs of this side
            :param outputs:    dictonary with the configuration of the inputs of a box, same possible keys as for inputs
            :param text_configuration: dictionary of arguments passed to the text
            :param level:      level of the component
        """

        # Get the position and size of the block
        if isinstance(position, (list, tuple)):
            size = (abs((position[1] - position[0]).x), abs((position[1] - position[0]).y))
            position = Point.get_mid(*position)

        super().__init__(position, text, size, text_configuration, level, *args, **kwargs)

        # Define inputs and outputs of the block
        input_dict = {
            'left': (
                self.left.add_y, 'west', self._size_y, inputs.get('left', 0), Input, inputs.get('left_space', None),
                inputs.get('left_text_space', 0.2), inputs.get('left_text', ())),
            'top': (
                self.top.add_x, 'north', self._size_x, inputs.get('top', 0), Input, inputs.get('top_space', None),
                inputs.get('top_text_space', 0.2), inputs.get('top_text', ())),
            'right': (
                self.right.add_y, 'east', self._size_y, inputs.get('right', 0), Input, inputs.get('right_space', None),
                inputs.get('right_text_space', 0.2), inputs.get('right_text', ())),
            'bottom': (
                self.bottom.add_x, 'south', self._size_x, inputs.get('bottom', 0), Input, inputs.get('bottom_space', None),
                inputs.get('bottom_text_space', 0.2), inputs.get('bottom_text', ()))
        }

        output_dict = {
            'left': (
                self.left.add_y, 'west', self._size_y, outputs.get('left', 0), Output, outputs.get('left_space', None),
                outputs.get('left_text_space', 0.2), outputs.get('left_text', ())),
            'top': (
                self.top.add_x, 'north', self._size_x, outputs.get('top', 0), Output, outputs.get('top_space', None),
                outputs.get('top_text_space', 0.2), outputs.get('top_text', ())),
            'right': (
                self.right.add_y, 'east', self._size_y, outputs.get('right', 0), Output, outputs.get('right_space', None),
                outputs.get('right_text_space', 0.2), outputs.get('right_text', ())),
            'bottom': (
                self.bottom.add_x, 'south', self._size_x, outputs.get('bottom', 0), Output, outputs.get('bottom_space', None),
                outputs.get('bottom_text_space', 0.2), outputs.get('bottom_text', ()))
        }

        self.set_in_output(input_dict, output_dict, self._get_in_output, level)

    @staticmethod
    def _get_in_output(in_out_dict):
        """Function to calculate the positions of the inputs and outputs"""
        pos_func, direction, size, count, in_out, space, _, _ = in_out_dict
        pos_list = Block.get_in_out_list(size, space, count)
        return [in_out.convert(pos_func(pos, direction)) for pos in pos_list]

    def build(self, pic):
        """Funtion to add the Latex code to the Latex document"""

        box = TikZDraw([self.top_left.tikz, 'rectangle', self.bottom_right.tikz],
                       TikZOptions(*self._style_args, **self._tikz_options))
        pic.append(box)
        super().build(pic)
