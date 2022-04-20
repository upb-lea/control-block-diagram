from control_block_diagram.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Connection


class Limit(PredefinedComponent):
    """
        Limitation Block
        Rectangular block with a limited graph
    """

    def __init__(self, position, size, level: int = 0, *box_args, **box_kwargs):
        """
            Initializes a limit block
                :param position:   position of the block
                :param size:       size of the block
                :param level:      level of the block
                :param box_args:   arguments passed to the box
                :param box_kwargs: keyword arguments passed to the box
        """

        super().__init__(position)

        self._box = Box(position, size, level=level, *box_args, **box_kwargs)

        bx = 0.1
        by = 0.1
        le = (1 - 2 * bx) / 3

        Connection([self._box.bottom_left.add(self._box.size_x * bx, self._box.size_y * by),
                    self._box.bottom_left.add(self._box.size_x * bx + le, self._box.size_y * by),
                    self._box.top_right.sub(self._box.size_x * bx + le, self._box.size_y * by),
                    self._box.top_right.sub(self._box.size_x * bx, self._box.size_y * by)], arrow=False, level=level)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border
