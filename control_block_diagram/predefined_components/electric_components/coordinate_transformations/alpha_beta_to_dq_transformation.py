from .coordinate_transformation import CoordinateTransformation


class AlphaBetaToDqTransformation(CoordinateTransformation):

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(bottom=1), additional_outputs: dict = dict(top=1),
                 input_space: float = 0.6, output_space: float = 0.6):
        super().__init__(position, size, r'$\alpha\beta$', '$dq$', input, 2, output, 2, additional_inputs,
                         additional_outputs, input_space, output_space)
