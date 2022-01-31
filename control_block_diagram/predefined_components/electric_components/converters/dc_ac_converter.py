from .converter import Converter


class DcAcConverter(Converter):
    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 in_out_space_right_left: float = 0, in_out_space_top_bottom: float = 0, doc=None):
        super().__init__(position, size, ['='], [r'$\sim$'], input, 2, output, 3, in_out_space_right_left,
                         in_out_space_top_bottom, doc)
