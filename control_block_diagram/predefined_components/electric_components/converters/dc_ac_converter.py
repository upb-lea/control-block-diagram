from .converter import Converter


class DcAcConverter(Converter):
    """
        DC-AC-Converter Block with 2 inputs and 3 outputs
    """

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.6,
                 output_space: float = 0.3, *args, **kwargs):
        """
        Initializes an DC-AC-Converter Block
            :param position:           position of the block
            :param size:               size of the block
            :param input:              side of the inputs
            :param output:             side of the outputs
            :param additional_inputs:  dictonary of additional inputs (s. Box)
            :param additional_outputs: dictonary of additional outputs (s. Box)
            :param input_space:        space between the inputs
            :param output_space:       space between the outputs
        """

        super().__init__(position, size, '=', r'$\sim$', input, 2, output, 3, additional_inputs, additional_outputs,
                         input_space, output_space, *args, **kwargs)
