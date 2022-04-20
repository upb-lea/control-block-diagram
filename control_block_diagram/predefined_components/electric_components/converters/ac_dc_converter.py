from .converter import Converter


class AcDcConverter(Converter):
    """
        AC-DC-Converter Block with 3 inputs and 2 outputs
    """

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.3,
                 output_space: float = 0.6, *args, **kwargs):
        """
        Initializes an AC-DC-Converter Block
            :param position:           position of the block
            :param size:               size of the block
            :param input:              side of the inputs
            :param output:             side of the outputs
            :param additional_inputs:  dictonary of additional inputs (s. Box)
            :param additional_outputs: dictonary of additional outputs (s. Box)
            :param input_space:        space between the inputs
            :param output_space:       space between the outputs
        """

        super().__init__(position, size, r'$\sim$', '=', input, 3, output, 2, additional_inputs, additional_outputs,
                         input_space, output_space, *args, **kwargs)
