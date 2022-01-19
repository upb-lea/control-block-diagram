from pylatex import TikZDraw, TikZOptions
from ..component import Component
from ..text import Text
from ..points import Point, Center


class Block(Component):

    @property
    def position(self):
        return self._position

    @property
    def size(self):
        return self._size_x, self._size_y

    @property
    def right(self):
        return self._position.add_x(self._size_x / 2, 'east')

    @property
    def left(self):
        return self._position.add_x(-self._size_x / 2, 'west')

    @property
    def top(self):
        return self._position.add_y(self._size_y / 2, 'north')

    @property
    def bottom(self):
        return self._position.add_y(-self._size_y / 2, 'south')

    @property
    def top_left(self):
        return self._position.add(-self._size_x / 2, self._size_y / 2)

    @property
    def bottom_right(self):
        return self._position.add(self._size_x / 2, -self._size_y / 2)

    @property
    def end(self):
        return self.right.add_x(self._space)

    @property
    def input(self):
        return self._input_left + self._input_top + self._input_right + self._input_bottom

    @property
    def input_left(self):
        return self._input_left

    @property
    def input_top(self):
        return self._input_top

    @property
    def input_right(self):
        return self._input_right

    @property
    def input_bottom(self):
        return self._input_bottom

    @property
    def output(self):
        return self._output_right + self._output_bottom + self._output_left + self._output_top

    @property
    def output_left(self):
        return self._output_left

    @property
    def output_top(self):
        return self._output_top

    @property
    def output_right(self):
        return self._output_right

    @property
    def output_bottom(self):
        return self._output_bottom

    def __init__(self, position: Point, fill: str, draw: str, text: Text, size: tuple, space: float, doc = None):
        super().__init__()
        self._position = position if isinstance(position, Center) else position.add_x(size[0] / 2)
        self._fill = fill
        self._draw = draw
        self._text = text
        (self._size_x, self._size_y) = size
        self._space = space
        self._input = []
        self._output = []

        self._input_left = []
        self._input_top = []
        self._input_bottom = []
        self._input_right = []

        self._output_left = []
        self._output_top = []
        self._output_bottom = []
        self._output_right = []

        self._plot_inout = False

        if isinstance(self._text, Text):
            self._text.define(position=Point(self._position.x, self._position.y),
                              size=(max(self._size_x, 0.3), max(self._size_y, 0.3)))

        if doc is not None:
            doc.append(self)

    def build(self, pic):
        if isinstance(self._text, Text):
            self._text.build(pic)

        if self._plot_inout:
            for input_ in self.input:
                circle = TikZDraw([input_.tikz, 'circle'],
                                  options=TikZOptions(radius=str(0.1) + 'cm', draw='red', fill='red'))
                pic.append(circle)

            for output_ in self.output:
                circle = TikZDraw([output_.tikz, 'circle'],
                                  options=TikZOptions(radius=str(0.1) + 'cm', draw='blue', fill='blue'))
                pic.append(circle)
