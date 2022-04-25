from pylatex import TikZDraw, TikZOptions, TikZPathList
from ..block import Block
from ...points import Point
from ...text import Text


class CustomBlock(Block):
    """Block with a custom shape"""

    @property
    def points(self):
        """Returns the points of a custom block"""
        return self._points

    @property
    def input_left(self):
        """Returns all inputs on the left side of a block as a list"""
        return self._input_left

    @input_left.setter
    def input_left(self, inputs_left):
        if all(isinstance(inp, Point) for inp in inputs_left):
            self._input_left = inputs_left

    @property
    def input_top(self):
        """Returns all inputs on the top side of a block as a list"""
        return self._input_top

    @input_top.setter
    def input_top(self, inputs_top):
        if all(isinstance(inp, Point) for inp in inputs_top):
            self._input_top = inputs_top

    @property
    def input_right(self):
        """Returns all inputs on the right side of a block as a list"""
        return self._input_right

    @input_right.setter
    def input_right(self, inputs_right):
        if all(isinstance(inp, Point) for inp in inputs_right):
            self._input_right = inputs_right

    @property
    def input_bottom(self):
        """Returns all inputs on the bottom side of a block as a list"""
        return self._input_bottom

    @input_bottom.setter
    def input_bottom(self, inputs_bottom):
        if all(isinstance(inp, Point) for inp in inputs_bottom):
            self._input_bottom = inputs_bottom

    @property
    def output_left(self):
        """Returns all outputs on the left side of a block as a list"""
        return self._output_left

    @property
    def output_top(self):
        """Returns all outputs on the top side of a block as a list"""
        return self._output_top

    @property
    def output_right(self):
        """Returns all outputs on the right side of a block as a list"""
        return self._output_right

    @property
    def output_bottom(self):
        """Returns all outputs on the bottom side of a block as a list"""
        return self._output_bottom

    def __init__(self, points: [Point], text: (Text, str) = None, text_configuration: dict = dict(), level: int = 0,
                 *args, **kwargs):
        """
        Initialization of a custom block

            :param points:      list of the corner points of the block
            :param text:        text inside the block
            :param text_configuration: dictionary of arguments passed to the text
            :param level:       level of the component
        """

        x_val = [p.x for p in points]
        y_val = [p.y for p in points]
        size = (max(x_val) - min(x_val), max(y_val) - min(y_val))
        position = Point.get_mid(*points)

        super().__init__(position, text, size, text_configuration, level, *args, **kwargs)
        self._points = points

    def build(self, pic):
        """Funtion to add the Latex code to the Latex document"""
        points = []
        for p in self._points:
            points.extend([p.tikz, '--'])
        points.extend([self._points[0].tikz, '--', self._points[1].tikz])
        custom_block = TikZDraw(points, TikZOptions(*self._style_args, **self._tikz_options))
        pic.append(custom_block)
        super().build(pic)
