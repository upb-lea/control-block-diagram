from .converter import Converter
from control_block_diagram.components import Connection


class DcConverter(Converter):
    def __init__(self, position, size: float = 1.5, input: str = 'left', input_number: int = 1, output: str = 'bottom',
                 output_number: int = 2, input_space: float = 0.6,  output_space: float = 0.3):

        additional_inputs = dict(top=2, top_space=size * 0.6)
        super().__init__(position, size, '', '', input, input_number, output, output_number, additional_inputs,
                         dict(), input_space, output_space)
        self._con_in = [Connection.connect(_input.add_y(0.4 * size), _input, arrow=False) for _input in
                        self._box.input_top]
        self._con_dc = Connection.connect(self._con_in[1].begin.add(-size * 0.1, size * 0.1),
                                          self._con_in[0].begin.add(size * 0.1, size * 0.1),
                                          text=r'$u_{\mbox{\tiny DC}}$')
