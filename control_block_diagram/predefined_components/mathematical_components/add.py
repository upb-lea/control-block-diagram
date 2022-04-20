from ..predefined_components import PredefinedComponent
from control_block_diagram.components import Circle


class Add(PredefinedComponent):
    """
        Circular addition block
    """

    def __init__(self, position, radius: float = 0.15, inputs: dict = dict(left=1, bottom=1),
                 outputs: dict = dict(right=1), circle_kwargs: dict = dict(), *args, **kwargs):
        """
        Initializes an Add block
            :param position:       position of the block
            :param radius:         radius of the circle
            :param inputs:         dictonary of inputs (s. circle)
            :param outputs:        dictonary of outputs (s. circle)
            :param circle_kwargs:  dictonary of arguments passed to the circle

        """
        super().__init__(position)
        self._circle = Circle(position, radius, inputs=inputs, outputs=outputs, *args, **circle_kwargs, **kwargs)

        self.input = self._circle.input_dict
        self.output = self._circle.output_dict
        self.border = self._circle.border
