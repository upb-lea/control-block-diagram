from .coordinate_transformation import CoordinateTransformation


class DqToAbcTransformation(CoordinateTransformation):

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(bottom=1), additional_outputs: dict = dict(top=1),
                 input_space: float = 0.6, output_space: float = 0.3, doc=None):
        super().__init__(position, size, ['$dq$'], ['$abc$'], input, 2, output, 3, additional_inputs,
                         additional_outputs, input_space, output_space, doc)
