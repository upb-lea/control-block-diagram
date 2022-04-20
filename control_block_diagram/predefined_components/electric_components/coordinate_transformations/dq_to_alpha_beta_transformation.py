from .coordinate_transformation import CoordinateTransformation


class DqToAlphaBetaTransformation(CoordinateTransformation):
    """
        Coordinate transformation from dq-Coordinates to alpha-beta-Coordinates with 2 inputs and 2 outputs
    """

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(bottom=1), additional_outputs: dict = dict(top=1),
                 input_space: float = 0.6, output_space: float = 0.6, *args, **kwargs):
        """
            :param position:           position of the block
            :param size:               size of the block
            :param input:              side of the inputs
            :param output:             side of the outputs
            :param additional_inputs:  dictonary of additional inputs (s. Box)
            :param additional_outputs: dictonary of additional outputs (s. Box)
            :param input_space:        space between the inputs
            :param output_space:       space between the outputs
        """

        super().__init__(position, size, r'$\mathrm{dq}$', r'$\upalpha\upbeta$', input, 2, output, 2,
                         additional_inputs, additional_outputs, input_space, output_space, *args, **kwargs)
