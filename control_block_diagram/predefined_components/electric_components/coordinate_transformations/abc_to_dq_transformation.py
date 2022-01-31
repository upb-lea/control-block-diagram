from .coordinate_transformation import CoordinateTransformation


class AbcToDqTransformation(CoordinateTransformation):

    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 in_out_space_right_left: float = 0, in_out_space_top_bottom: float = 0,
                 additional_input: str = 'bottom', additional_output: str = 'top', doc=None):
        super().__init__(position, size, ['$abc$'], ['$dq$'], input, 3, output, 2, in_out_space_right_left,
                         in_out_space_top_bottom, additional_input, additional_output, doc)
