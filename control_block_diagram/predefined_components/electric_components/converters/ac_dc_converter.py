from .converter import Converter


class AcDcConverter(Converter):
    def __init__(self, position, size: float = 1.5, input: str = 'left', output: str = 'right',
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.3,
                 output_space: float = 0.6):
        super().__init__(position, size, r'$\sim$', '=', input, 3, output, 2, additional_inputs, additional_outputs,
                         input_space, output_space)