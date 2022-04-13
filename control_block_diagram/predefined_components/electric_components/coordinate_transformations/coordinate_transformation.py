from control_block_diagram.predefined_components.predefined_components import PredefinedComponent
from control_block_diagram import Box, Connection, Text


class CoordinateTransformation(PredefinedComponent):
    """
        Base class for coordinate transformations
        Square Block with diagonal
    """
    def __init__(self, position, size: float = 1.5, text_input: (str, iter) = '', text_output: (str, iter) = '',
                 input: str = 'left', input_number: int = 2, output: str = 'right', output_number: int = 2,
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.3,
                 output_space: float = 0.3, *args, **kwargs):
        """
        Initializes a coordinate transformation
            position:           position of the block
            size:               size of the block
            text_input:         text at the inputs
            text_output:        text at the outputs
            input:              side of the inputs
            input_number:       number of the inputs
            output:             side of the outputs
            output_number:      number of the outputs
            additional_inputs:  dictonary of additional inputs (s. Box)
            additional_outputs: dictonary of additional outputs (s. Box)
            input_space:        space between the inputs
            output_space:       space between the outputs
        """

        super().__init__(position)
        additional_inputs[input] = input_number
        additional_inputs[input + '_space'] = input_space
        additional_outputs[output] = output_number
        additional_outputs[output + '_space'] = output_space

        self._box = Box(position, (size, size), inputs=additional_inputs, outputs=additional_outputs, *args, **kwargs)
        self._diagonal = Connection([self._box.bottom_left, self._box.top_right], arrow=False, *args, **kwargs)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border

        pos_text_input = self._box.top_left.add(size / 4, -size / 4)
        pos_text_output = self._box.bottom_right.add(-size/4, size/4)
        if input in ['right', 'bottom']:
            (pos_text_input, pos_text_output) = (pos_text_output, pos_text_input)

        self._text_input = Text(text_input, position=pos_text_input, *args, **kwargs)
        self._text_output = Text(text_output, position=pos_text_output, *args, **kwargs)
