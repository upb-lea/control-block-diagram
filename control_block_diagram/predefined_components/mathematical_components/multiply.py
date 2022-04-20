from ..predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Connection


class Multiply(PredefinedComponent):
    """
        Rectangular multiply block with a cross
    """

    def __init__(self, position, size: tuple = (0.4, 0.4), inputs: dict = dict(left=1, bottom=1),
                 outputs: dict = dict(right=1), box_kwargs: dict = dict(), cross_kwargs: dict = dict(), *args,
                 **kwargs):
        """
        Initializes a multiply block
            :param position:       position of the multiply block
            :param size:           size of the multiply block
            :param inputs:         inputs of the multiply block (s. box)
            :param outputs:        outputs of the multiply block (s. box)
            :param box_kwargs:     arguments passed to the box
            :param cross_kwargs:   arguments passed to the cross
        """

        super().__init__(position)

        self._box = Box(position, size, inputs=inputs, outputs=outputs, *args, **box_kwargs, **kwargs)

        cross_size = 0.5 * min(*size) / 2
        self._con_1 = Connection([position.add(-cross_size, cross_size), position.add(cross_size, -cross_size)],
                                 arrow=False, line_width='thick', *args, **cross_kwargs, **kwargs)
        self._con_2 = Connection([position.sub(cross_size, cross_size), position.add(cross_size, cross_size)],
                                 arrow=False, line_width='thick', *args, **cross_kwargs, **kwargs)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border
