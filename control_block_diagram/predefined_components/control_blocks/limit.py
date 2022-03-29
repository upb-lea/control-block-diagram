from control_block_diagram.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Connection


class Limit(PredefinedComponent):
    def __init__(self, position, size, *box_args, **box_kwargs):
        super().__init__(position)

        self._box = Box(position, size, *box_args, **box_kwargs)

        bx = 0.1
        by = 0.1
        le = (1 - 2 * bx) / 3

        Connection([self._box.bottom_left.add(self._box.size_x * bx, self._box.size_y * by),
                    self._box.bottom_left.add(self._box.size_x * bx + le, self._box.size_y * by),
                    self._box.top_right.sub(self._box.size_x * bx + le, self._box.size_y * by),
                    self._box.top_right.sub(self._box.size_x * bx, self._box.size_y * by)], arrow=False)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border
