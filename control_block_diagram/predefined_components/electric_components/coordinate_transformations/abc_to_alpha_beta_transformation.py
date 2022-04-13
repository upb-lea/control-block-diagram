from .coordinate_transformation import CoordinateTransformation


class AbcToAlphaBetaTransformation(CoordinateTransformation):
    """
        Coordinate transformation from abc-Coordinates to alpha-beta-Coordinates with 3 inputs and 2 outputs
    """

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(),  input_space: float = 0.3,
                 output_space: float = 0.6, *args, **kwargs):
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

        super().__init__(position, size, r'$\mathrm{abc}$', r'$\upalpha\upbeta$', input, 3, output, 2,
                         additional_inputs, additional_outputs, input_space, output_space, *args, **kwargs)
