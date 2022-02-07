from control_block_diagram.components.component import Component


class PredefinedComponent(Component):

    @property
    def position(self):
        return self._position

    @property
    def input(self):
        return self._input_left + self._input_top + self._input_right + self._input_bottom

    @input.setter
    def input(self, inputs):
        self._input_left = inputs['left']
        self._input_top = inputs['top']
        self._input_right = inputs['right']
        self._input_bottom = inputs['bottom']

    @property
    def input_dict(self):
        return dict(left=self._input_left, top=self._input_top, right=self._input_right, bottom=self._input_bottom)

    @property
    def input_left(self):
        return self._input_left

    @input_left.setter
    def input_left(self, input_left):
        self._input_left = input_left

    @property
    def input_top(self):
        return self._input_top

    @input_top.setter
    def input_top(self, input_top):
        self._input_top = input_top

    @property
    def input_right(self):
        return self._input_right

    @input_right.setter
    def input_right(self, input_right):
        self._input_right = input_right

    @property
    def input_bottom(self):
        return self._input_bottom

    @input_bottom.setter
    def input_bottom(self, input_bottom):
        self._input_bottom = input_bottom

    @property
    def output(self):
        return self._output_left + self._output_top + self._output_right + self._output_bottom

    @output.setter
    def output(self, outputs):
        self._output_left = outputs['left']
        self._output_top = outputs['top']
        self._output_right = outputs['right']
        self._output_bottom = outputs['bottom']

    @property
    def output_dict(self):
        return dict(left=self._output_left, top=self._output_top, right=self._output_right, bottom=self._output_bottom)

    @property
    def output_left(self):
        return self._output_left

    @output_left.setter
    def output_left(self, output_left):
        self._output_left = output_left

    @property
    def output_top(self):
        return self._output_top

    @output_top.setter
    def output_top(self, output_top):
        self._output_top = output_top

    @property
    def output_right(self):
        return self._output_right

    @output_right.setter
    def output_right(self, output_right):
        self._output_right = output_right

    @property
    def output_bottom(self):
        return self._output_bottom

    @output_bottom.setter
    def output_bottom(self, output_bottom):
        self._output_bottom = output_bottom

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, top):
        self._top = top

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, bottom):
        self._bottom = bottom

    @property
    def border(self):
        return dict(left=self._left, top=self._top, right=self._right, bottom=self._bottom)

    @border.setter
    def border(self, border_dict):
        self._left = border_dict['left']
        self._top = border_dict['top']
        self._right = border_dict['right']
        self._bottom = border_dict['bottom']

    def __init__(self, position, doc=None):
        super().__init__(doc)

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

    def build(self, pic):
        pass
