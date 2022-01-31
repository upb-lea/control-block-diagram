from pylatex import TikZDraw, TikZOptions, TikZPathList
from ..block import Block
from ...points import Point, Input, Output, Center
from ...text import Text


class Triangle(Block):

    def __init__(self, position: (Point, Center), size: tuple = (2.5, 1.5), text: Text = None, fill: str = 'white',
                 draw: str = 'black', space: float = 1.5, inputs: dict = dict(left=1), outputs: dict = dict(right=1),
                 doc=None):
        super().__init__(position, fill, draw, text, size, space, doc)

        input_dict = {'left': (
            self.left.add_y, 'west', self._size_y, inputs.get('left', 0), Input, inputs.get('left_space', None), inputs.get('left_text', ())),
            'top': (
                self.top.add_x, 'north', self._size_x, inputs.get('top', 0), Input, inputs.get('top_space', None), inputs.get('top_text', ())),
            'right': (
                self.right.add_y, 'east', self._size_y, inputs.get('right', 0), Input, inputs.get('right_space', None), inputs.get('right_text', ())),
            'bottom': (
                self.bottom.add_x, 'south', self._size_x, inputs.get('bottom', 0), Input, inputs.get('bottom_space', None),
                inputs.get('bottom_text', ()))}

        output_dict = {'left': (
            self.left.add_y, 'west', self._size_y, outputs.get('left', 0), Output, outputs.get('left_space', None), outputs.get('left_text', ())),
            'top': (
                self.top.add_x, 'north', self._size_x, outputs.get('top', 0), Output, outputs.get('top_space', None), outputs.get('top_text', ())),
            'right': (
                self.right.add_y, 'east', self._size_y, outputs.get('right', 0), Output, outputs.get('right_space', None), outputs.get('right_text', ())),
            'bottom': (
                self.bottom.add_x, 'south', self._size_x, outputs.get('bottom', 0), Output, outputs.get('bottom_space', None),
                outputs.get('bottom_text', ()))}

        self.set_in_output(input_dict, output_dict, self._get_in_output)
        self._text.define(position=self.position.add_x(-self.size[0] / 4))

    def _get_in_output(self, in_out_dict):
        pos_func, direction, size, count, in_out, space, _ = in_out_dict
        if space is None:
            return [in_out.convert(pos_func((0.5 - (i + 1) / (count + 1)) * size, direction)) for i in range(count)]
        else:
            if count > 1:
                space = (size - 2 * space) / (count - 1)
                return [in_out.convert(pos_func((0.5 - (i / (count - 1))) * space, direction)) for i in range(count)]
            elif count == 1:
                return [in_out.convert(pos_func(0, direction))]
            else:
                return []

    def build(self, pic):

        triangle = TikZDraw([self.top_left.tikz, '--', self.right.tikz, '--', self.bottom_left.tikz, '--',
                             self.top_left.tikz], TikZOptions(draw=self._draw, fill=self._fill))
        pic.append(triangle)
        super().build(pic)

