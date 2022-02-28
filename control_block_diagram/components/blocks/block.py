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
    def top_right(self):
        return self._position.add(self._size_x / 2, self._size_y / 2)

    @property
    def bottom_left(self):
        return self._position.add(-self._size_x / 2, -self._size_y / 2)

    @property
    def bottom_right(self):
        return self._position.add(self._size_x / 2, -self._size_y / 2)

    @property
    def input(self):
        return self._input_left + self._input_top + self._input_right + self._input_bottom

    @property
    def input_dict(self):
        return dict(left=self._input_left, top=self._input_top, right=self._input_right, bottom=self._input_bottom)

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
    def output_dict(self):
        return dict(left=self._output_left, top=self._output_top, right=self._output_right, bottom=self._output_bottom)

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

    @property
    def border(self):
        return dict(left=self.left.x, top=self.top.y, right=self.right.x, bottom=self.bottom.y)

    def __init__(self, position: Point, text: (Text, str), size: tuple, **block_configuration):
        super().__init__()
        self._position = position

        if isinstance(position, Center):
            if position.vertical:
                self._position = self._position.add_x(size[0] / 2)
            if position.horizontal:
                self._position = self._position.sub_y(size[1] / 2)

        self._tikz_options = dict()

        fill = block_configuration.get('fill', self._configuration['fill'])
        draw = block_configuration.get('draw', self._configuration['draw'])
        self._line_width = block_configuration.get('line_width', self._configuration['line_width'])

        if isinstance(fill, str):
            self._tikz_options['fill'] = fill
        if isinstance(draw, str):
            self._tikz_options['draw'] = draw

        self._text = text if isinstance(text, Text) else Text(text)
        (self._size_x, self._size_y) = size

        self._set_border(self.top_left, self.top_right, self.bottom_left, self.bottom_right)

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

        self._input_left_text = []
        self._input_top_text = []
        self._input_bottom_text = []
        self._input_right_text = []

        self._output_left_text = []
        self._output_top_text = []
        self._output_bottom_text = []
        self._output_right_text = []

        self._plot_inout = False

        if isinstance(self._text, Text):
            self._text.define(position=Point(self._position.x, self._position.y),
                              size=(max(self._size_x, 0.3), max(self._size_y, 0.3)))

    def set_in_output(self, input_dict, output_dict, get_position):
        self._input_left = get_position(input_dict['left'])
        self._input_top = get_position(input_dict['top'])
        self._input_right = get_position(input_dict['right'])
        self._input_bottom = get_position(input_dict['bottom'])

        self._output_left = get_position(output_dict['left'])
        self._output_top = get_position(output_dict['top'])
        self._output_right = get_position(output_dict['right'])
        self._output_bottom = get_position(output_dict['bottom'])

        self._input_left_text = self.set_in_out_text(self._input_left, input_dict['left'][-1], input_dict['left'][-2],
                                                     Point.add_x)
        self._input_top_text = self.set_in_out_text(self._input_top, input_dict['top'][-1][::-1], input_dict['top'][-2],
                                                    Point.sub_y)
        self._input_right_text = self.set_in_out_text(self._input_right, input_dict['right'][-1],
                                                      input_dict['right'][-2], Point.sub_x)
        self._input_bottom_text = self.set_in_out_text(self._input_top, input_dict['bottom'][-1][::-1],
                                                       input_dict['bottom'][-2], Point.add_y)

        self._output_left_text = self.set_in_out_text(self._output_left, output_dict['left'][-1],
                                                      output_dict['left'][-2],  Point.add_x)
        self._output_top_text = self.set_in_out_text(self._output_top, output_dict['top'][-1][::-1],
                                                     output_dict['top'][-2], Point.sub_y)
        self._output_right_text = self.set_in_out_text(self._output_right, output_dict['right'][-1],
                                                       output_dict['right'][-2], Point.sub_x)
        self._output_bottom_text = self.set_in_out_text(self._input_top, output_dict['bottom'][-1][::-1],
                                                        output_dict['bottom'][-2], Point.add_y)

        self._input_top = self._input_top[::-1]
        self._input_bottom = self._input_bottom[::-1]
        self._output_top = self._output_top[::-1]
        self._output_bottom = self._output_bottom[::-1]

    @staticmethod
    def get_in_out_list(size: float, space: float, number: int):
        if number == 0:
            return []
        if number == 1:
            return [0]
        if space is None or space == 0:
            space = size / (number + 1)
        elif size < space * (number - 1):
            space = size / (number - 1)
        begin = (number - 1) * space
        return [begin - ((number - 1) / 2 + i) * space for i in range(number)]

    @staticmethod
    def set_in_out_text(point, text, space, add):
        space = 0 if space is None else space
        return [Text(text_, add(point_, space)) for point_, text_ in zip(point, text)]

    def build(self, pic):
        pass
