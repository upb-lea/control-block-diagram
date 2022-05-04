class PredefinedComponent:
    """
        A predefined component can contain several components, which are either completely predefined or receive the
        corresponding parameters when instantiated.
    """

    @property
    def position(self):
        """Returns the position of a predefined component"""
        return self._position

    @property
    def input(self):
        """Returns the inputs of a predefined component"""
        return self._input_left + self._input_top + self._input_right + self._input_bottom

    @input.setter
    def input(self, inputs):
        """Sets the inputs of a predefined component"""
        self._input_left = inputs.get('left', [])
        self._input_top = inputs.get('top', [])
        self._input_right = inputs.get('right', [])
        self._input_bottom = inputs.get('bottom', [])

    @property
    def input_dict(self):
        """Returns the inputs of a predefined component in a dictonary"""
        return dict(left=self._input_left, top=self._input_top, right=self._input_right, bottom=self._input_bottom)

    @property
    def input_left(self):
        """Returns the left input of a predefined component"""
        return self._input_left

    @input_left.setter
    def input_left(self, input_left):
        """Sets the left input of a predefined component"""
        self._input_left = input_left

    @property
    def input_top(self):
        """Returns the to input of a predefined component"""
        return self._input_top

    @input_top.setter
    def input_top(self, input_top):
        """Sets the top input of a predefined component"""
        self._input_top = input_top

    @property
    def input_right(self):
        """Returns the right input of a predefined component"""
        return self._input_right

    @input_right.setter
    def input_right(self, input_right):
        """Sets the right input of a predefined component"""
        self._input_right = input_right

    @property
    def input_bottom(self):
        """Returns the bottom input of a predefined component"""
        return self._input_bottom

    @input_bottom.setter
    def input_bottom(self, input_bottom):
        """Sets the bottom input of a predefined component"""
        self._input_bottom = input_bottom

    @property
    def output(self):
        """Returns the outputs of a predefined component"""
        return self._output_left + self._output_top + self._output_right + self._output_bottom

    @output.setter
    def output(self, outputs):
        """Sets the outputs of a predefined component"""
        self._output_left = outputs.get('left', [])
        self._output_top = outputs.get('top', [])
        self._output_right = outputs.get('right', [])
        self._output_bottom = outputs.get('bottom', [])

    @property
    def output_dict(self):
        """Returns the outputs of a predefined component as a dictonary"""
        return dict(left=self._output_left, top=self._output_top, right=self._output_right, bottom=self._output_bottom)

    @property
    def output_left(self):
        """Returns the left output of a predefined component"""
        return self._output_left

    @output_left.setter
    def output_left(self, output_left):
        """Sets the left input of a predefined component"""
        self._output_left = output_left

    @property
    def output_top(self):
        """Returns the top output of a predefined component"""
        return self._output_top

    @output_top.setter
    def output_top(self, output_top):
        """Sets the top input of a predefined component"""
        self._output_top = output_top

    @property
    def output_right(self):
        """Returns the right output of a predefined component"""
        return self._output_right

    @output_right.setter
    def output_right(self, output_right):
        """Sets the right input of a predefined component"""
        self._output_right = output_right

    @property
    def output_bottom(self):
        """Returns the bottom output of a predefined component"""
        return self._output_bottom

    @output_bottom.setter
    def output_bottom(self, output_bottom):
        """Sets the bottom input of a predefined component"""
        self._output_bottom = output_bottom

    @property
    def left(self):
        """Returns the left border of a predefined component"""
        return self._left

    @left.setter
    def left(self, left):
        """Sets the left border of a predefined component"""
        self._left = left

    @property
    def top(self):
        """Returns the top border of a predefined component"""
        return self._top

    @top.setter
    def top(self, top):
        """Sets the top border of a predefined component"""
        self._top = top

    @property
    def right(self):
        """Returns the right border of a predefined component"""
        return self._right

    @right.setter
    def right(self, right):
        """Sets the right border of a predefined component"""
        self._right = right

    @property
    def bottom(self):
        """Returns the bottom border of a predefined component"""
        return self._bottom

    @bottom.setter
    def bottom(self, bottom):
        """Sets the bottom border of a predefined component"""
        self._bottom = bottom

    @property
    def border(self):
        """Returns the border of a predefined component as a dictonary"""
        return dict(left=self._left, top=self._top, right=self._right, bottom=self._bottom)

    @border.setter
    def border(self, border_dict):
        """Sets the border of a predefined component"""
        self._left = border_dict['left']
        self._top = border_dict['top']
        self._right = border_dict['right']
        self._bottom = border_dict['bottom']

    def __init__(self, position):
        """Initializes a predefined component"""

        self._position = position

        self._input_left = []
        self._input_top = []
        self._input_right = []
        self._input_bottom = []

        self._output_left = []
        self._output_top = []
        self._output_right = []
        self._output_bottom = []

        self._left = None
        self._top = None
        self._right = None
        self._bottom = None
