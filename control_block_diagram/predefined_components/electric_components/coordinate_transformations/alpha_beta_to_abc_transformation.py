from .coordinate_transformation import CoordinateTransformation


class AlphaBetaToAbcTransformation(CoordinateTransformation):
    """
        Coordinate transformation from alpha-beta-Coordinates to abc-Coordinates with 2 inputs and 3 outputs
    """

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.6,
                 output_space: float = 0.3, *args, **kwargs):
        """
            position:           position of the block
            size:               size of the block
            input:              side of the inputs
            output:             side of the outputs
            additional_inputs:  dictonary of additional inputs (s. Box)
            additional_outputs: dictonary of additional outputs (s. Box)
            input_space:        space between the inputs
            output_space:       space between the outputs
        """

        super().__init__(position, size, r'$\upalpha\upbeta$', r'$\mathrm{abc}$', input, 2, output, 3,
                         additional_inputs, additional_outputs, input_space, output_space, *args, **kwargs)
