from .coordinate_transformation import CoordinateTransformation


class AlphaBetaToAbcTransformation(CoordinateTransformation):

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.6,
                 output_space: float = 0.3, doc=None):
        super().__init__(position, size, [r'$\alpha\beta$'], ['$abc$'], input, 2, output, 3, additional_inputs,
                         additional_outputs, input_space, output_space, doc)
