from pylatex import TikZDraw, TikZOptions
from ..block import Block
from ...points import Point, Input, Output, Center
from ...text import Text


class Box(Block):
    def __init__(self, position: (Point, Center), size: tuple = (2.5, 1.5), text: Text = None, fill: str = 'white',
                 draw: str = 'black', space: float = 1.5, input_left: int = 1, input_top: int = 0, input_right: int = 0,
                 input_bottom: int = 0, output_left: int = 0, output_top: int = 0, output_right: int = 1,
                 output_bottom: int = 0, input_output_space: int = None, input_text: (list, tuple) = (), doc=None):
        super().__init__(position, fill, draw, text, size, space, doc)
        self._input_output_space = input_output_space
        self._define_in_output(input_left, input_top, input_right, input_bottom, output_left, output_top, output_right,
                               output_bottom)
        self._input_text = [Text([text], pos.add_x(0.15), fontsize='\small', doc=doc) for text, pos in zip(input_text, self.input)]

    def _define_in_output(self, input_left: int, input_top: int, input_right: int, input_bottom: int, output_left: int,
                          output_top: int, output_right: int, output_bottom: int):
        in_out_dict = {'left': (self.left.add_y, 'west', self._size_y),
                       'top': (self.top.add_x, 'north', self._size_x),
                       'right': (self.right.add_y, 'east', self._size_y),
                       'bottom': (self.bottom.add_x, 'south', self._size_x)}

        self._input_left = self._get_in_output(in_out_dict['left'], Input.convert, input_left)
        self._input_top = self._get_in_output(in_out_dict['top'], Input.convert, input_top)
        self._input_right = self._get_in_output(in_out_dict['right'], Input.convert, input_right)
        self._input_bottom = self._get_in_output(in_out_dict['bottom'], Input.convert, input_bottom)

        self._output_left = self._get_in_output(in_out_dict['left'], Output.convert, output_left)
        self._output_top = self._get_in_output(in_out_dict['top'], Output.convert, output_top)
        self._output_right = self._get_in_output(in_out_dict['right'], Output.convert, output_right)
        self._output_bottom = self._get_in_output(in_out_dict['bottom'], Output.convert, output_bottom)

    def _get_in_output(self, in_out_dict, in_out=Input.convert, count: int = 0):
        pos_func, direction, size = in_out_dict
        if self._input_output_space is None:
            return [in_out(pos_func((0.5 - (i + 1) / (count + 1)) * size, direction)) for i in range(count)]
        else:
            if count > 1:
                space = (size - 2 * self._input_output_space) / (count - 1)
                return [in_out(pos_func((0.5 - (i / (count - 1))) * space, direction)) for i in range(count)]
            elif count == 1:
                return [in_out(pos_func(0, direction))]
            else:
                return []

    def build(self, pic):
        box = TikZDraw([self.top_left.tikz, 'rectangle', self.bottom_right.tikz],
                       TikZOptions(draw=self._draw, fill=self._fill))
        pic.append(box)
        for input_text in self._input_text:
            input_text.build(pic)
        super().build(pic)
