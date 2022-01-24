from control_block_diagram.components.component import Component


class PredefinedComponent(Component):

    @property
    def input(self):
        return self._input_left + self._input_top + self._input_right + self._input_bottom

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

    def __init__(self):
        self._input_left = []
        self._input_top = []
        self._input_right = []
        self._input_bottom = []

        self._output_left = []
        self._output_top = []
        self._output_right = []
        self._output_bottom = []

    def build(self, pic):
        pass
