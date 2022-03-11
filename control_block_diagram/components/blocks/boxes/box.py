from pylatex import TikZDraw, TikZOptions
from ..block import Block
from ...points import Point, Input, Output
from ...text import Text


class Box(Block):
    def __init__(self, position: (Point, list, tuple), size: tuple = (2.5, 1.5), text: (Text, str) = None,
                 inputs: dict = dict(left=1), outputs: dict = dict(right=1), **block_configuration):

        if isinstance(position, (list, tuple)):
            size = (abs((position[1] - position[0]).x), abs((position[1] - position[0]).y))
            position = Point.get_mid(*position)

        super().__init__(position, text, size, **block_configuration)

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

        self.set_in_output(input_dict, output_dict, self._get_in_output)

    @staticmethod
    def _get_in_output(in_out_dict):
        pos_func, direction, size, count, in_out, space, _, _ = in_out_dict
        pos_list = Block.get_in_out_list(size, space, count)
        return [in_out.convert(pos_func(pos, direction)) for pos in pos_list]

    def build(self, pic):
        box = TikZDraw([self.top_left.tikz, 'rectangle', self.bottom_right.tikz],
                       TikZOptions(self._line_width, **self._tikz_options))
        pic.append(box)
        super().build(pic)
