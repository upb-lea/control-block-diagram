from ..component import Component
from ..text import Text
from ..points import Point, Center


class Block(Component):
    """Base class for a block with trigonometric form"""

    @property
    def position(self):
        """Returns the center of a shape"""
        return self._position

    @property
    def size(self):
        """Returns the size in x and y direction of a shape"""
        return self._size_x, self._size_y

    @property
    def size_x(self):
        """Returns the size in x direction of a shape"""
        return self._size_x

    @property
    def size_y(self):
        """Returns the size in y direction of a shape"""
        return self._size_y

    @property
    def right(self):
        """Returns the point of the right center of the block"""
        return self._position.add_x(self._size_x / 2, 'east')

    @property
    def left(self):
        """Returns the point of the left center of the block"""
        return self._position.add_x(-self._size_x / 2, 'west')

    @property
    def top(self):
        """Returns the point of the top center of the block"""
        return self._position.add_y(self._size_y / 2, 'north')

    @property
    def bottom(self):
        """Returns the point of the bottom center of the block"""
        return self._position.add_y(-self._size_y / 2, 'south')

    @property
    def top_left(self):
        """Returns the point of the top left corner of the block"""
        return self._position.add(-self._size_x / 2, self._size_y / 2)

    @property
    def top_right(self):
        """Returns the point of the top right corner of the block"""
        return self._position.add(self._size_x / 2, self._size_y / 2)

    @property
    def bottom_left(self):
        """Returns the point of the bottom left corner of the block"""
        return self._position.add(-self._size_x / 2, -self._size_y / 2)

    @property
    def bottom_right(self):
        """Returns the point of the bottom right corner of the block"""
        return self._position.add(self._size_x / 2, -self._size_y / 2)

    @property
    def input(self):
        """Returns all inputs of a block as a list"""
        return self._input_left + self._input_top + self._input_right + self._input_bottom

    @property
    def input_dict(self):
        """Returns all inputs of a block as a dictonary"""
        return dict(left=self._input_left, top=self._input_top, right=self._input_right, bottom=self._input_bottom)

    @property
    def input_left(self):
        """Returns all inputs on the left side of a block as a list"""
        return self._input_left

    @property
    def input_top(self):
        """Returns all inputs on the top side of a block as a list"""
        return self._input_top

    @property
    def input_right(self):
        """Returns all inputs on the right side of a block as a list"""
        return self._input_right

    @property
    def input_bottom(self):
        """Returns all inputs on the bottom side of a block as a list"""
        return self._input_bottom

    @property
    def output(self):
        """Returns all outputs of a block as a list"""
        return self._output_right + self._output_bottom + self._output_left + self._output_top

    @property
    def output_dict(self):
        """Returns all outputs of a block as a dictonary"""
        return dict(left=self._output_left, top=self._output_top, right=self._output_right, bottom=self._output_bottom)

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

    @property
    def border(self):
        """Returns the boundaries of a block as dictonary"""
        return dict(left=self.left.x, top=self.top.y, right=self.right.x, bottom=self.bottom.y)

    def __init__(self, position: Point, text: (Text, str), size: tuple, text_configuration: dict = dict(),
                 level: int = 0, *args, **kwargs):
        """
            Initializes a block and sets the default parameters

            :param position:    position of the block
            :param text:        text inside the block
            :param size:        size of the block
            :param text_configuration: dictionary of arguments passed to the text
            :param level:       level of the block
        """

        super().__init__(level, *args, **kwargs)

        # Set the position
        self._position = position
        if isinstance(position, Center):
            if position.vertical:
                self._position = self._position.add_x(size[0] / 2)
            if position.horizontal:
                self._position = self._position.sub_y(size[1] / 2)

        # Set the default parameter
        self._tikz_options = dict()

        fill = kwargs.get('fill', self._configuration['fill'])
        draw = kwargs.get('draw', self._configuration['draw'])
        rounded_corners = kwargs.get('rounded_corners', self._configuration['rounded_corners'])
        line_width = kwargs.get('line_width', self._configuration['line_width'])
        line_style = kwargs.get('line_style', self._configuration['line_style'])
        self._style_args = []

        if isinstance(fill, str):
            self._tikz_options['fill'] = fill
        if isinstance(draw, str):
            self._tikz_options['draw'] = draw
        elif draw is None:
            self._tikz_options['draw'] = fill
        if isinstance(rounded_corners, str):
            self._tikz_options['rounded corners'] = rounded_corners
        if isinstance(line_width, str):
            if line_width in ['ultra thin', 'very thin', 'thin', 'semithick', 'thick', 'very thick', 'ultra thick']:
                self._style_args.append(line_width)
            else:
                self._tikz_options['line width'] = line_width
        if isinstance(line_style, str):
            self._style_args.append(line_style)

        self._text = Text(text, level=level, text_configuration=text_configuration)     # Set the text
        (self._size_x, self._size_y) = size     # Set the size
        self._text_size = text_configuration.get('size', (max(self._size_x, 0.3), max(self._size_y, 0.3)))
        self._set_border(self.top_left, self.top_right, self.bottom_left, self.bottom_right)    # Set the border

        # Create lists for the inputs and outputs
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

        # Define the text of a block
        if isinstance(self._text, Text):
            self._text.define(position=Point(self._position.x, self._position.y),
                              size=self._text_size)

    def set_in_output(self, input_dict, output_dict, get_position, level=0, *args, **kwargs):
        """Set the inputs and outputs of a block, with a given function for getting the right positions"""

        # Set the positions of the in- and outputs
        self._input_left = get_position(input_dict['left'])
        self._input_top = get_position(input_dict['top'])
        self._input_right = get_position(input_dict['right'])
        self._input_bottom = get_position(input_dict['bottom'])
        self._output_left = get_position(output_dict['left'])
        self._output_top = get_position(output_dict['top'])
        self._output_right = get_position(output_dict['right'])
        self._output_bottom = get_position(output_dict['bottom'])

        # Set the texts of the in- and outputs
        self._input_left_text = self.set_in_out_text(self._input_left, input_dict['left'][-1], input_dict['left'][-2],
                                                     Point.add_x, level=level)
        self._input_top_text = self.set_in_out_text(self._input_top, input_dict['top'][-1][::-1], input_dict['top'][-2],
                                                    Point.sub_y, level=level)
        self._input_right_text = self.set_in_out_text(self._input_right, input_dict['right'][-1],
                                                      input_dict['right'][-2], Point.sub_x, level=level)
        self._input_bottom_text = self.set_in_out_text(self._input_bottom, input_dict['bottom'][-1][::-1],
                                                       input_dict['bottom'][-2], Point.add_y, level=level)

        self._output_left_text = self.set_in_out_text(self._output_left, output_dict['left'][-1],
                                                      output_dict['left'][-2],  Point.add_x, level=level)
        self._output_top_text = self.set_in_out_text(self._output_top, output_dict['top'][-1][::-1],
                                                     output_dict['top'][-2], Point.sub_y, level=level)
        self._output_right_text = self.set_in_out_text(self._output_right, output_dict['right'][-1],
                                                       output_dict['right'][-2], Point.sub_x, level=level)
        self._output_bottom_text = self.set_in_out_text(self._output_bottom, output_dict['bottom'][-1][::-1],
                                                        output_dict['bottom'][-2], Point.add_y, level=level)

        # Reverse the list so that the inputs and outputs can be output in the correct order
        self._input_top = self._input_top[::-1]
        self._input_bottom = self._input_bottom[::-1]
        self._output_top = self._output_top[::-1]
        self._output_bottom = self._output_bottom[::-1]

    @staticmethod
    def get_in_out_list(size: float, space: float, number: int):
        """Funtion to get a list of the in- and outputs positions in one direction"""
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
    def set_in_out_text(point, text, space, add, level=0, *args, **kwargs):
        """Function to add a text to an in- or output"""
        space = 0 if space is None else space
        return [Text(text_, add(point_, space), level=level) for point_, text_ in zip(point, text)]

    def build(self, pic):
        """Generates the code which will be written into the latex file"""
        pass
