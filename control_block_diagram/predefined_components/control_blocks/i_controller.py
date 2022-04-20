from control_block_diagram.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Connection, Text


class IController(PredefinedComponent):
    """
        Integration Controller Block
        Rectangular block with coordinate system and graph with constant slope
    """

    def __init__(self, position, size: tuple = (1.5, 1), text: str = None, text_configuration: dict = {},
                 input: str = 'left', input_number: int = 1, output: str = 'right', output_number: int = 1,
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.3,
                 output_space: float = 0.3, *args, **kwargs):
        """
        Initializes an integration controller block
            :param position:           position of the block
            :param size:               size of the block
            :param text:               text above the block
            :param text_configuration: arguments passed to the text above
            :param input:              side of the inputs
            :param input_number:       number of inputs
            :param output:             side of the outputs
            :param output_number:      number of outputs
            :param additional_inputs:  dictonary of additional inputs (s. Box)
            :param additional_outputs: dictonary of additional outputs (s. Box)
            :param input_space:        space between the inputs
            :param output_space:       space between the outputs
        """

        super().__init__(position)
        additional_inputs[input] = input_number
        additional_inputs[input + '_space'] = input_space
        additional_outputs[output] = output_number
        additional_outputs[output + '_space'] = output_space

        self._box = Box(position, size=size, inputs=additional_inputs, outputs=additional_outputs, *args, **kwargs)

        self._connection1 = Connection([self._box.top_left.add(size[0] * 0.06, -size[1] * 0.09),
                                        self._box.bottom_left.add(size[0] * 0.06, size[1] * 0.09),
                                        self._box.bottom_right.add(-size[0] * 0.06, size[1] * 0.09)], arrow=False,
                                       *args, **kwargs)
        self._connection2 = Connection([self._box.bottom_left.add(size[0] * 0.06, size[1] * 0.09),
                                        self._box.top_right.add(-size[0] * 0.06, -size[1] * 0.2)], arrow=False,
                                       *args, **kwargs)

        if text is not None:
            self._text = Text(text, position.add_y(size[1]), text_configuration=text_configuration, *args, **kwargs)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border
